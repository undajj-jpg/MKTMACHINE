# 05 — Calendario de 100 días

Meta global: **100 clientes**. Metas acumuladas de control: día 30 → 12 · día 50 → 30 · día 75 → 62 · día 100 → 100.
La curva no es lineal: los primeros 30 días construyen la máquina; los últimos 50 producen el 70% de los cierres.

## Fase 0 — Fundaciones (días 1–7) · Meta: 0 clientes, máquina lista

- [ ] Arreglos críticos de la web (docs/01: uptime, prerender, og:image, WhatsApp, precios visibles)
- [ ] Comprar 3 dominios de envío + crear 6 buzones + SPF/DKIM/DMARC (docs/03)
- [ ] **Iniciar warm-up** (corre en paralelo 14 días)
- [ ] Configurar `.env`, probar los 5 scripts end-to-end con `--dry-run`
- [ ] Generar primeras listas: `find_leads.py` en 3 ciudades × 4 rubros → objetivo **1.000 leads ICP-1/2**
- [ ] Enriquecer y verificar emails (`enrich_leads.py` + verificador)
- [ ] Preparar 2–3 casos de portfolio (aunque sean proyectos propios/demo)

## Fase 1 — Encendido (días 8–14) · Meta acumulada: 2–3 clientes

- Warm-up continúa; **todavía sin volumen de email**.
- **Empezar por los canales que no necesitan warm-up**: WhatsApp (20/día) y LinkedIn (15 invitaciones/día) sobre los mejores leads ICP-1.
- Primeras respuestas → primeras llamadas → primeros cierres (los leads sin web cierran rápido).
- Pulir guiones con lo aprendido en las primeras 50 conversaciones.

## Fase 2 — Rampa de email (días 15–30) · Meta acumulada: 12

- Email a 50%: 40–60 nuevos/día + follow-ups. WhatsApp y LinkedIn a tope.
- A/B test de asuntos y ángulos (2 variantes por ICP, mínimo 100 envíos por variante antes de decidir).
- Introducir el **mockup vendedor** en toque 3 para leads calientes.
- Viernes: revisión de métricas (`track.py stats`) + ajuste.
- **Hito día 30**: 12 clientes. Si <8: revisar oferta y respuesta antes de subir volumen (subir volumen con mal mensaje solo quema lista).

## Fase 3 — Régimen completo (días 31–60) · Meta acumulada: 40

- Email a régimen: 100–150 nuevos/día con 3 dominios + follow-ups automáticos.
- Nuevas listas cada semana: +2 ciudades o +2 rubros (`find_leads.py`), mantener 500+ leads frescos en cola.
- **Activar motor de referidos**: cada cliente cerrado recibe la oferta "1 mes gratis por cada negocio referido que contrate".
- Publicar 2 casos de éxito reales de la campaña en la web + LinkedIn.
- Empezar **canal partners**: contactar 20 contadores/gestorías/agencias de marketing locales — ellos tienen decenas de clientes sin web; comisión 15% recurrente o fee por referido.
- **Hito día 50**: 30 clientes (mitad del tiempo, ~1/3 de la meta — correcto por la curva).

## Fase 4 — Escala (días 61–85) · Meta acumulada: 75

- Duplicar lo que funciona: el ICP con mejor tasa de cierre se lleva el 70% del volumen.
- Referidos + partners deberían aportar 2–4 clientes/semana ya.
- Remarketing de lista: re-contactar con ángulo nuevo a los "no respondió" de hace 45+ días (secuencia corta de 2 toques).
- Considerar 1 asistente virtual (~$400/mes) para prospección manual de WhatsApp/Instagram si el cuello de botella es tiempo.

## Fase 5 — Sprint final (días 86–100) · Meta acumulada: 100

- Oferta de cierre para el pipeline tibio: "setup gratis contratando el plan anual" o "20% el primer trimestre" — solo a quienes ya mostraron interés y no cerraron.
- Barrer TODO el pipeline: cada lead en etapa `interesado`/`llamada` recibe un último toque personal.
- Documentar el playbook ganador (asuntos, ángulos, rubros, ciudades con mejor conversión) para el siguiente ciclo.

## Ritual diario (bloques, ~4–5 h)

| Hora | Bloque |
|---|---|
| 09:00–09:30 | Responder TODAS las respuestas de la noche |
| 09:30–10:30 | WhatsApp del día (20–30) + LinkedIn (15) |
| 10:30–11:00 | Lanzar envío de email del día (`send_campaign.py`) |
| 11:00–13:00 | Llamadas de 15 min + cierres + mockups |
| 17:00–17:30 | Segunda pasada de respuestas + actualizar `track.py` |

## Ritual semanal (viernes)

1. `track.py stats` → comparar contra la meta de la fase.
2. Decidir 1 solo cambio grande para la semana siguiente (ángulo, rubro, ciudad, oferta).
3. Generar y verificar la lista de la semana entrante.
