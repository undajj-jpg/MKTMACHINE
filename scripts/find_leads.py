#!/usr/bin/env python3
"""Encuentra negocios locales SIN web (o con "web" que es una red social)
usando Google Places API (New) — el ICP-1 de la campaña.

Uso:
    python find_leads.py --query "dentista en Valencia" --out ../data/leads.csv
    python find_leads.py --query "restaurante en Rosario" --max 60 --incluir-con-web

Salida: CSV acumulativo (no duplica place_id ya presentes) con columnas:
    negocio, nombre, telefono, email, web, red_social, rubro, ciudad,
    icp, fuente, fecha_alta, place_id, rating, num_resenas, estado
"""

import argparse
import csv
import os
import sys
import time
from datetime import date
from pathlib import Path

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_URL = "https://places.googleapis.com/v1/places:searchText"
FIELDS = ",".join([
    "places.id",
    "places.displayName",
    "places.websiteUri",
    "places.nationalPhoneNumber",
    "places.internationalPhoneNumber",
    "places.formattedAddress",
    "places.rating",
    "places.userRatingCount",
    "nextPageToken",
])

SOCIAL_DOMAINS = (
    "facebook.com", "instagram.com", "linktr.ee", "wa.me", "whatsapp.com",
    "twitter.com", "x.com", "tiktok.com", "bit.ly", "linkin.bio",
)

CSV_COLUMNS = [
    "negocio", "nombre", "telefono", "email", "web", "red_social", "rubro",
    "ciudad", "icp", "fuente", "fecha_alta", "place_id", "rating",
    "num_resenas", "estado", "primera_linea", "hallazgos", "variante",
]


def clasificar_web(url: str) -> tuple[str, str]:
    """Devuelve (web_real, red_social) según el campo websiteUri."""
    if not url:
        return "", ""
    low = url.lower()
    for dom in SOCIAL_DOMAINS:
        if dom in low:
            return "", url
    return url, ""


def buscar(api_key: str, query: str, max_results: int) -> list[dict]:
    resultados, page_token = [], None
    while len(resultados) < max_results:
        body = {"textQuery": query, "pageSize": min(20, max_results - len(resultados))}
        if page_token:
            body["pageToken"] = page_token
        resp = requests.post(
            API_URL,
            json=body,
            headers={
                "X-Goog-Api-Key": api_key,
                "X-Goog-FieldMask": FIELDS,
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        if resp.status_code != 200:
            print(f"[!] Error {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
            break
        data = resp.json()
        resultados.extend(data.get("places", []))
        page_token = data.get("nextPageToken")
        if not page_token:
            break
        time.sleep(2)  # el token de página tarda unos segundos en activarse
    return resultados


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--query", required=True, help='ej: "dentista en Valencia"')
    ap.add_argument("--out", default="../data/leads.csv")
    ap.add_argument("--max", type=int, default=60, help="máximo de resultados (default 60)")
    ap.add_argument("--incluir-con-web", action="store_true",
                    help="incluir también negocios con web propia (ICP-2, para auditar)")
    args = ap.parse_args()

    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not api_key:
        sys.exit("Falta GOOGLE_PLACES_API_KEY (ver .env.example)")

    partes = args.query.split(" en ")
    rubro = partes[0].strip()
    ciudad = partes[1].strip() if len(partes) > 1 else ""

    out = Path(args.out)
    existentes: set[str] = set()
    filas: list[dict] = []
    if out.exists():
        with out.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                existentes.add(row.get("place_id", ""))
                filas.append(row)

    lugares = buscar(api_key, args.query, args.max)
    nuevos = sin_web = 0
    for p in lugares:
        pid = p.get("id", "")
        if pid in existentes:
            continue
        web, red_social = clasificar_web(p.get("websiteUri", ""))
        if web and not args.incluir_con_web:
            continue  # solo queremos ICP-1 (sin web) salvo flag
        icp = "ICP-1" if not web else "ICP-2"
        if not web:
            sin_web += 1
        filas.append({
            "negocio": p.get("displayName", {}).get("text", ""),
            "nombre": "",
            "telefono": p.get("nationalPhoneNumber") or p.get("internationalPhoneNumber", ""),
            "email": "",
            "web": web,
            "red_social": red_social,
            "rubro": rubro,
            "ciudad": ciudad,
            "icp": icp,
            "fuente": "Google Maps",
            "fecha_alta": date.today().isoformat(),
            "place_id": pid,
            "rating": p.get("rating", ""),
            "num_resenas": p.get("userRatingCount", ""),
            "estado": "nuevo",
            "primera_linea": "",
            "hallazgos": "",
            "variante": "",
        })
        existentes.add(pid)
        nuevos += 1

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in filas:
            writer.writerow({c: row.get(c, "") for c in CSV_COLUMNS})

    print(f"[ok] {nuevos} leads nuevos ({sin_web} sin web) → {out} (total {len(filas)})")


if __name__ == "__main__":
    main()
