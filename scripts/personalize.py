#!/usr/bin/env python3
"""Genera la primera línea personalizada de cada email con la API de Claude,
usando los datos reales del lead (rubro, ciudad, rating, reseñas, hallazgos).

Rellena la columna `primera_linea` del CSV. Solo procesa leads que aún no
la tienen.

Uso:
    python personalize.py --in ../data/leads.csv
    python personalize.py --in ../data/leads.csv --limit 50
"""

import argparse
import csv
import sys
from pathlib import Path

import anthropic

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODEL = "claude-opus-4-8"

SYSTEM = """Escribes primeras líneas de cold emails en español para dev.lop, \
un estudio que hace webs y software con planes mensuales todo incluido.

Reglas estrictas:
- UNA sola frase (máximo 25 palabras), tono cercano y natural, tuteo neutro.
- Debe referirse a un dato REAL y concreto del negocio (rubro, ciudad, \
rating, cantidad de reseñas, o un hallazgo de su web). Nada genérico.
- Prohibido: halagos vacíos ("me encanta tu negocio"), jerga de marketing, \
emojis, signos de exclamación dobles, mencionar que usamos IA.
- No repitas la propuesta comercial (eso viene después en el email).
- Devuelve SOLO la frase, sin comillas ni explicación.

Ejemplos del estilo buscado:
- "Vi que tienen 4,8 estrellas con más de 200 reseñas en Google — claramente \
el trabajo habla por ustedes."
- "Entre los talleres de Palermo, el suyo es de los mejor puntuados en Maps."
- "Revisando webs de clínicas en Valencia, la suya fue de las pocas que no \
carga bien desde el móvil."
"""


def prompt_lead(row: dict) -> str:
    datos = [
        f"Negocio: {row.get('negocio', '')}",
        f"Rubro: {row.get('rubro', '')}",
        f"Ciudad: {row.get('ciudad', '')}",
    ]
    if row.get("rating"):
        datos.append(f"Rating en Google: {row['rating']} ({row.get('num_resenas', '?')} reseñas)")
    if row.get("red_social"):
        datos.append(f"Su 'web' en Google Maps apunta a: {row['red_social']}")
    if row.get("web"):
        datos.append(f"Web: {row['web']}")
    if row.get("hallazgos"):
        datos.append(f"Problemas detectados en su web:\n{row['hallazgos']}")
    return ("Escribe la primera línea del email para este lead:\n\n"
            + "\n".join(datos))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="infile", default="../data/leads.csv")
    ap.add_argument("--limit", type=int, default=0, help="máximo de leads a procesar")
    args = ap.parse_args()

    path = Path(args.infile)
    if not path.exists():
        sys.exit(f"No existe {path}")

    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY del entorno

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columnas = reader.fieldnames or []
        filas = list(reader)

    hechas = 0
    for row in filas:
        if row.get("primera_linea") or not row.get("negocio"):
            continue
        if args.limit and hechas >= args.limit:
            break
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=300,
                system=[{
                    "type": "text",
                    "text": SYSTEM,
                    "cache_control": {"type": "ephemeral"},
                }],
                messages=[{"role": "user", "content": prompt_lead(row)}],
            )
            if resp.stop_reason == "refusal":
                print(f"[!] {row['negocio']}: solicitud rechazada, se omite")
                continue
            linea = next(
                (b.text for b in resp.content if b.type == "text"), ""
            ).strip().strip('"')
            if linea:
                row["primera_linea"] = linea
                hechas += 1
                print(f"[ok] {row['negocio']}: {linea}")
        except anthropic.RateLimitError:
            print("[!] Rate limit — guardando progreso y saliendo", file=sys.stderr)
            break
        except anthropic.APIStatusError as e:
            print(f"[!] {row['negocio']}: error API {e.status_code}", file=sys.stderr)
        except anthropic.APIConnectionError:
            print("[!] Error de conexión — guardando progreso", file=sys.stderr)
            break

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(filas)

    print(f"[ok] {hechas} primeras líneas generadas → {path}")


if __name__ == "__main__":
    main()
