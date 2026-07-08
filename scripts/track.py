#!/usr/bin/env python3
"""CRM mínimo de la campaña en SQLite (data/crm.sqlite).

Etapas del pipeline:
    nuevo → contactado → respondio → interesado → llamada → cliente
    (terminales: baja, no_interesado, perdido)

Uso:
    python track.py set correo@negocio.com respondio --nota "pidió precios"
    python track.py set correo@negocio.com cliente --valor 59
    python track.py baja correo@negocio.com
    python track.py list interesado
    python track.py stats
"""

import argparse
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "crm.sqlite"

ETAPAS = ["nuevo", "contactado", "respondio", "interesado", "llamada",
          "cliente", "no_interesado", "perdido", "baja"]

META_DIAS = {30: 12, 50: 30, 75: 62, 100: 100}


def db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS pipeline (
        email TEXT PRIMARY KEY, negocio TEXT, etapa TEXT, valor_mensual REAL,
        nota TEXT, actualizado TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS historial (
        id INTEGER PRIMARY KEY, fecha TEXT, email TEXT, etapa TEXT, nota TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS envios (
        id INTEGER PRIMARY KEY, fecha TEXT, email TEXT, negocio TEXT,
        campana TEXT, asunto TEXT, buzon TEXT, estado TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS bajas (
        email TEXT PRIMARY KEY, fecha TEXT)""")
    return con


def cmd_set(con, args):
    if args.etapa not in ETAPAS:
        sys.exit(f"Etapa inválida. Opciones: {', '.join(ETAPAS)}")
    ahora = datetime.now().isoformat(timespec="seconds")
    con.execute("""INSERT INTO pipeline (email, negocio, etapa, valor_mensual, nota, actualizado)
        VALUES (?,?,?,?,?,?)
        ON CONFLICT(email) DO UPDATE SET
            etapa=excluded.etapa,
            negocio=COALESCE(NULLIF(excluded.negocio,''), pipeline.negocio),
            valor_mensual=COALESCE(excluded.valor_mensual, pipeline.valor_mensual),
            nota=excluded.nota, actualizado=excluded.actualizado""",
        (args.email.lower(), args.negocio or "", args.etapa, args.valor, args.nota or "", ahora))
    con.execute("INSERT INTO historial (fecha, email, etapa, nota) VALUES (?,?,?,?)",
                (ahora, args.email.lower(), args.etapa, args.nota or ""))
    con.commit()
    print(f"[ok] {args.email} → {args.etapa}")


def cmd_baja(con, args):
    ahora = datetime.now().isoformat(timespec="seconds")
    con.execute("INSERT OR REPLACE INTO bajas (email, fecha) VALUES (?,?)",
                (args.email.lower(), ahora))
    con.execute("""INSERT INTO pipeline (email, etapa, actualizado) VALUES (?,?,?)
        ON CONFLICT(email) DO UPDATE SET etapa='baja', actualizado=excluded.actualizado""",
                (args.email.lower(), "baja", ahora))
    con.commit()
    print(f"[ok] {args.email} dado de baja — no volverá a contactarse")


def cmd_list(con, args):
    q = "SELECT email, negocio, etapa, valor_mensual, nota, actualizado FROM pipeline"
    params = ()
    if args.etapa:
        q += " WHERE etapa=?"
        params = (args.etapa,)
    q += " ORDER BY actualizado DESC"
    filas = con.execute(q, params).fetchall()
    if not filas:
        print("(vacío)")
        return
    for email, negocio, etapa, valor, nota, act in filas:
        v = f" ${valor:.0f}/mes" if valor else ""
        n = f" — {nota}" if nota else ""
        print(f"{act[:10]}  [{etapa:<13}] {negocio or email}{v}{n}")


def cmd_stats(con, args):
    print("=" * 52)
    print("  MKTMACHINE — Estado de campaña")
    print("=" * 52)

    total_envios = con.execute(
        "SELECT COUNT(*) FROM envios WHERE estado='enviado'").fetchone()[0]
    semana = (datetime.now() - timedelta(days=7)).isoformat()
    envios_semana = con.execute(
        "SELECT COUNT(*) FROM envios WHERE estado='enviado' AND fecha>=?",
        (semana,)).fetchone()[0]
    print(f"\nEmails enviados: {total_envios} (últimos 7 días: {envios_semana})")

    print("\nPipeline:")
    conteos = dict(con.execute(
        "SELECT etapa, COUNT(*) FROM pipeline GROUP BY etapa").fetchall())
    for etapa in ETAPAS:
        n = conteos.get(etapa, 0)
        if n:
            print(f"  {etapa:<14} {n:>4}  {'█' * min(n, 40)}")

    contactados = total_envios or sum(
        conteos.get(e, 0) for e in ETAPAS if e != "nuevo")
    respondieron = sum(conteos.get(e, 0) for e in
                       ("respondio", "interesado", "llamada", "cliente", "no_interesado"))
    clientes = conteos.get("cliente", 0)
    if contactados:
        print(f"\nTasa de respuesta: {100 * respondieron / contactados:.1f}%"
              f"  ·  Tasa de cierre sobre contactados: {100 * clientes / contactados:.2f}%")

    mrr = con.execute("SELECT COALESCE(SUM(valor_mensual),0) FROM pipeline "
                      "WHERE etapa='cliente'").fetchone()[0]
    print(f"\nCLIENTES: {clientes} / 100   ·   MRR: ${mrr:,.0f}/mes")

    primera = con.execute("SELECT MIN(fecha) FROM historial").fetchone()[0]
    if primera:
        dia = (datetime.now() - datetime.fromisoformat(primera)).days + 1
        print(f"Día de campaña: {dia}")
        proxima = next(((d, m) for d, m in sorted(META_DIAS.items()) if d >= dia), None)
        if proxima:
            d, m = proxima
            ritmo = "✅ en ritmo" if clientes >= m * dia / d else "⚠️ por debajo del ritmo"
            print(f"Próxima meta: {m} clientes al día {d} — {ritmo}")
    print()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("set", help="actualizar etapa de un lead")
    p.add_argument("email")
    p.add_argument("etapa", choices=ETAPAS)
    p.add_argument("--negocio", default="")
    p.add_argument("--valor", type=float, default=None, help="valor mensual del plan (USD)")
    p.add_argument("--nota", default="")

    p = sub.add_parser("baja", help="opt-out permanente")
    p.add_argument("email")

    p = sub.add_parser("list", help="listar pipeline")
    p.add_argument("etapa", nargs="?", choices=ETAPAS)

    sub.add_parser("stats", help="métricas y avance hacia los 100")

    args = ap.parse_args()
    con = db()
    try:
        {"set": cmd_set, "baja": cmd_baja, "list": cmd_list, "stats": cmd_stats}[args.cmd](con, args)
    finally:
        con.close()


if __name__ == "__main__":
    main()
