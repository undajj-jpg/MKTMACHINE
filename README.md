# MKTMACHINE — 100 clientes en 100 días para dev.lop

Máquina de adquisición de clientes por outbound (cold email + WhatsApp + LinkedIn) para [devlop.it](https://devlop.it/): webs, software a medida y automatización con planes mensuales de suscripción.

## El objetivo

**100 clientes nuevos en 100 días** (1 cliente/día de media). Producto de entrada: Presencia Web (desde $49 + plan mensual $29–199/mes con cambios incluidos). El plan mensual convierte cada cierre en ingreso recurrente: 100 clientes ≈ **$3.000–6.000 USD/mes de MRR** al final del período.

## La matemática del funnel

| Canal | Volumen (100 días) | Tasa respuesta | Oportunidades | Cierre | Clientes |
|---|---|---|---|---|---|
| Cold email | 10.000 contactos | 3–5% | 105–175 | 40–50% | **45–85** |
| WhatsApp | 2.000 contactos | 15–20% | 60–80 | 40% | **24–32** |
| LinkedIn | 1.500 invitaciones | 30% aceptan | 40–50 | 40% | **16–20** |
| Referidos (desde día 30) | clientes existentes | — | — | — | **10–15** |

**Total esperado: 95–150 clientes.** El objetivo es alcanzable, pero exige disciplina diaria: ~120 emails, ~25 WhatsApp y ~15 invitaciones de LinkedIn por día una vez completado el warm-up.

## Estructura del repo

```
docs/
  01-analisis-web.md          Auditoría de devlop.it + arreglos de conversión (hacer ANTES de enviar tráfico)
  02-estrategia.md            ICPs, oferta de entrada, ángulos de ataque, funnel completo
  03-entregabilidad.md        Dominios, SPF/DKIM/DMARC, warm-up, límites de envío
  04-legal.md                 RGPD/LSSI, CAN-SPAM, reglas por país, opt-out obligatorio
  05-calendario-100-dias.md   Plan semana a semana con metas numéricas
playbooks/
  emails.md                   Secuencias completas de cold email por ICP (4 secuencias × 4 toques)
  whatsapp-linkedin.md        Guiones de WhatsApp y LinkedIn
  objeciones-cierre.md        Manejo de objeciones, guion de llamada de 15 min, cierre
scripts/
  find_leads.py               Encuentra negocios SIN web (o con web mala) vía Google Places API
  enrich_leads.py             Audita la web de cada lead y extrae emails de contacto
  personalize.py              Genera primeras líneas personalizadas con la API de Claude
  send_campaign.py            Envía campañas por SMTP con throttling, opt-out y logging
  track.py                    CRM en SQLite: pipeline, etapas, métricas y reporte semanal
data/
  leads.sample.csv            Formato de ejemplo del archivo de leads
```

## Quickstart

```bash
cd scripts
pip install -r requirements.txt
cp .env.example .env          # completar claves y SMTP

# 1. Conseguir leads (negocios sin web en una ciudad/rubro)
python find_leads.py --query "dentista en Valencia" --out ../data/leads.csv

# 2. Enriquecer: auditar webs existentes y extraer emails
python enrich_leads.py --in ../data/leads.csv

# 3. Personalizar primera línea con IA
python personalize.py --in ../data/leads.csv

# 4. Enviar (empieza SIEMPRE con --dry-run)
python send_campaign.py --leads ../data/leads.csv --template ../playbooks/templates/icp1_email1.txt --dry-run

# 5. Trackear el pipeline
python track.py stats
```

## Reglas de oro

1. **No enviar ni un email hasta terminar el warm-up** (docs/03) — quemar el dominio en la semana 1 mata la campaña entera.
2. **Nunca enviar desde devlop.it** — usar dominios secundarios (devlop-web.com, getdevlop.com…).
3. **Todo email lleva opt-out y firma real** (docs/04). Baja solicitada = baja inmediata.
4. **Responder cada respuesta en <2 horas** en horario laboral. La velocidad de respuesta es el multiplicador más grande del funnel.
5. **Registrar todo en track.py** — lo que no se mide, no se mejora. Revisión de métricas cada viernes.
