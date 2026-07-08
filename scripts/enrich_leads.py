#!/usr/bin/env python3
"""Enriquece leads: audita la web de cada lead (ICP-2) y extrae emails de
contacto. Rellena las columnas `email` y `hallazgos` del CSV.

Uso:
    python enrich_leads.py --in ../data/leads.csv
"""

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
EMAIL_BLOCKLIST = ("example.", "sentry.", "wixpress", ".png", ".jpg", ".webp", "@2x")

PAGINAS_CONTACTO = ("contacto", "contact", "sobre-nosotros", "about", "quienes-somos")


def fetch(url: str, timeout: int = 15) -> requests.Response | None:
    try:
        return requests.get(url, headers={"User-Agent": UA}, timeout=timeout,
                            allow_redirects=True)
    except requests.RequestException:
        return None


def extraer_emails(html: str) -> list[str]:
    emails = set()
    for m in EMAIL_RE.findall(html):
        low = m.lower()
        if not any(b in low for b in EMAIL_BLOCKLIST):
            emails.add(low)
    return sorted(emails)


def auditar(url: str) -> tuple[list[str], str, list[str]]:
    """Devuelve (hallazgos, hallazgo_principal, emails)."""
    hallazgos: list[str] = []
    if url.startswith("http://"):
        url_https = url.replace("http://", "https://", 1)
        if fetch(url_https) is None:
            hallazgos.append("— Sin candado de seguridad (HTTPS): Chrome la marca 'No segura'")

    resp = fetch(url)
    if resp is None:
        return (["— La web no carga (probé varias veces y da error)"], "que la web no carga", [])
    if resp.status_code >= 400:
        return ([f"— La web devuelve error {resp.status_code}"], "que la web da error", [])

    html = resp.text
    low = html.lower()

    if resp.elapsed.total_seconds() > 4:
        hallazgos.append(f"— Tarda {resp.elapsed.total_seconds():.1f}s en cargar "
                         "(cada segundo extra pierde ~7% de visitas)")
    if 'name="viewport"' not in low:
        hallazgos.append("— No se adapta a móvil (60%+ de tus visitas entran desde el celular)")

    anios_viejos = re.findall(r"(?:©|&copy;|copyright)\D{0,10}(20[01]\d|202[0-3])", low)
    if anios_viejos:
        hallazgos.append(f"— El pie dice © {min(anios_viejos)}: transmite negocio abandonado")

    for gen, nombre in (("wix.com", "Wix"), ("wordpress", "WordPress sin actualizar"),
                        ("jimdo", "Jimdo"), ("frontpage", "FrontPage")):
        if gen in low and "generator" in low:
            hallazgos.append(f"— Hecha con {nombre}: diseño genérico y difícil de posicionar")
            break
    if "<title>" not in low or re.search(r"<title>\s*(home|inicio|untitled)?\s*</title>", low):
        hallazgos.append("— Sin título optimizado para Google (SEO básico ausente)")

    emails = extraer_emails(html)
    if not emails:
        base = f"{urlparse(resp.url).scheme}://{urlparse(resp.url).netloc}"
        for pagina in PAGINAS_CONTACTO:
            r2 = fetch(urljoin(base + "/", pagina))
            if r2 is not None and r2.status_code == 200:
                emails = extraer_emails(r2.text)
                if emails:
                    break

    principal = hallazgos[0].lstrip("— ").lower() if hallazgos else ""
    return hallazgos[:3], principal, emails


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="infile", default="../data/leads.csv")
    args = ap.parse_args()

    path = Path(args.infile)
    if not path.exists():
        sys.exit(f"No existe {path}")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columnas = reader.fieldnames or []
        filas = list(reader)

    procesadas = con_email = 0
    for row in filas:
        web = (row.get("web") or "").strip()
        if not web or row.get("hallazgos"):
            continue
        if not web.startswith("http"):
            web = "https://" + web
        print(f"[.] Auditando {web} ...")
        hallazgos, _principal, emails = auditar(web)
        row["hallazgos"] = "\n".join(hallazgos)
        if emails and not row.get("email"):
            row["email"] = emails[0]
            con_email += 1
        procesadas += 1

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(filas)

    print(f"[ok] {procesadas} webs auditadas, {con_email} emails nuevos → {path} "
          f"({date.today().isoformat()})")


if __name__ == "__main__":
    main()
