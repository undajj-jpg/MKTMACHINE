#!/usr/bin/env python3
"""Envía una campaña de cold email por SMTP con protecciones de
entregabilidad: throttling aleatorio, tope diario, exclusión de bajas,
cabecera List-Unsubscribe y registro de cada envío en el CRM (SQLite).

SIEMPRE probar primero con --dry-run.

Uso:
    python send_campaign.py --leads ../data/leads.csv \
        --template ../playbooks/templates/icp1_email1.txt --dry-run

    python send_campaign.py --leads ../data/leads.csv \
        --template ../playbooks/templates/icp1_email1.txt --campana icp1-t1
"""

import argparse
import csv
import os
import random
import re
import smtplib
import sqlite3
import sys
import time
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DB_PATH = Path(__file__).parent.parent / "data" / "crm.sqlite"
FIRMA_PATH = Path(__file__).parent.parent / "playbooks" / "templates" / "firma.txt"
VAR_RE = re.compile(r"\{\{(\w+)\}\}")


def db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS envios (
        id INTEGER PRIMARY KEY, fecha TEXT, email TEXT, negocio TEXT,
        campana TEXT, asunto TEXT, buzon TEXT, estado TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS bajas (
        email TEXT PRIMARY KEY, fecha TEXT)""")
    return con


def cargar_template(path: Path) -> tuple[str, str]:
    texto = path.read_text(encoding="utf-8")
    primera, _, resto = texto.partition("\n")
    if not primera.lower().startswith("subject:"):
        sys.exit(f"El template {path} debe empezar con 'Subject: ...'")
    return primera[len("subject:"):].strip(), resto.strip()


def render(plantilla: str, variables: dict) -> tuple[str, list[str]]:
    faltantes: list[str] = []

    def sub(m: re.Match) -> str:
        clave = m.group(1)
        valor = variables.get(clave, "")
        if not valor:
            faltantes.append(clave)
        return str(valor)

    return VAR_RE.sub(sub, plantilla), faltantes


def enviados_hoy(con: sqlite3.Connection, buzon: str) -> int:
    hoy = datetime.now().strftime("%Y-%m-%d")
    row = con.execute(
        "SELECT COUNT(*) FROM envios WHERE buzon=? AND fecha LIKE ? AND estado='enviado'",
        (buzon, hoy + "%")).fetchone()
    return row[0]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--leads", required=True)
    ap.add_argument("--template", required=True)
    ap.add_argument("--campana", default="", help="etiqueta de la campaña (ej. icp1-t1)")
    ap.add_argument("--dry-run", action="store_true", help="muestra sin enviar")
    ap.add_argument("--max", type=int, default=0, help="tope de esta ejecución")
    args = ap.parse_args()

    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    remitente = os.environ.get("REMITENTE_NOMBRE", "dev.lop")
    max_dia = int(os.environ.get("MAX_ENVIOS_DIA", "40"))

    if not args.dry_run and (not smtp_user or not smtp_pass):
        sys.exit("Faltan SMTP_USER/SMTP_PASS (ver .env.example)")

    asunto_tpl, cuerpo_tpl = cargar_template(Path(args.template))
    firma_tpl = FIRMA_PATH.read_text(encoding="utf-8") if FIRMA_PATH.exists() else ""
    campana = args.campana or Path(args.template).stem

    con = db()
    bajas = {r[0] for r in con.execute("SELECT email FROM bajas")}
    ya_contactados = {
        r[0] for r in con.execute(
            "SELECT email FROM envios WHERE campana=? AND estado='enviado'", (campana,))
    }

    cupo = max_dia - enviados_hoy(con, smtp_user)
    if args.max:
        cupo = min(cupo, args.max)
    if cupo <= 0:
        sys.exit(f"Tope diario alcanzado para {smtp_user} ({max_dia}). Mañana más.")

    with open(args.leads, newline="", encoding="utf-8") as f:
        leads = list(csv.DictReader(f))

    smtp = None
    if not args.dry_run:
        smtp = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
        smtp.starttls()
        smtp.login(smtp_user, smtp_pass)

    enviados = saltados = 0
    try:
        for row in leads:
            if enviados >= cupo:
                print(f"[i] Cupo de la ejecución alcanzado ({cupo}).")
                break
            email = (row.get("email") or "").strip().lower()
            if not email:
                continue
            if email in bajas:
                saltados += 1
                continue
            if email in ya_contactados:
                continue
            verificado = (row.get("email_verificado") or "ok").lower()
            if verificado not in ("ok", "valid", ""):
                saltados += 1
                continue

            variables = dict(row)
            variables.setdefault("remitente_nombre", remitente)
            variables["firma"], _ = render(firma_tpl, variables)
            variables.setdefault("nombre", row.get("nombre") or "")
            if not variables["nombre"]:
                variables["nombre"] = row.get("negocio", "")

            asunto, falt_a = render(asunto_tpl, variables)
            cuerpo, falt_c = render(cuerpo_tpl, variables)
            faltantes = set(falt_a + falt_c) - {"nombre"}
            if faltantes:
                print(f"[skip] {email}: faltan variables {sorted(faltantes)}")
                saltados += 1
                continue

            if args.dry_run:
                print(f"\n===== DRY RUN → {email} =====\nSubject: {asunto}\n\n{cuerpo}\n")
                enviados += 1
                continue

            msg = EmailMessage()
            msg["From"] = f"{remitente} <{smtp_user}>"
            msg["To"] = email
            msg["Subject"] = asunto
            msg["List-Unsubscribe"] = f"<mailto:{smtp_user}?subject=baja>"
            msg.set_content(cuerpo)

            try:
                smtp.send_message(msg)
                estado = "enviado"
                enviados += 1
                print(f"[ok] {enviados}/{cupo} → {email}")
            except smtplib.SMTPException as e:
                estado = f"error: {e}"
                print(f"[!] {email}: {e}", file=sys.stderr)

            con.execute(
                "INSERT INTO envios (fecha, email, negocio, campana, asunto, buzon, estado) "
                "VALUES (?,?,?,?,?,?,?)",
                (datetime.now().isoformat(timespec="seconds"), email,
                 row.get("negocio", ""), campana, asunto, smtp_user, estado))
            con.commit()
            time.sleep(random.uniform(120, 300))  # 2–5 min entre envíos
    finally:
        if smtp is not None:
            smtp.quit()
        con.close()

    modo = "DRY RUN — nada enviado" if args.dry_run else "enviados"
    print(f"\n[fin] {enviados} {modo}, {saltados} saltados (bajas/sin datos/no verificados)")


if __name__ == "__main__":
    main()
