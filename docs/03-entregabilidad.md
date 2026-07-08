# 03 — Entregabilidad: que los emails lleguen a la bandeja de entrada

El 90% de los cold emails que fracasan, fracasan aquí. Esta configuración es OBLIGATORIA antes de enviar el primer email.

## 1. Dominios de envío (nunca el principal)

**Jamás enviar cold email desde @devlop.it.** Si el dominio cae en listas negras, mueren también los emails transaccionales del portal de clientes.

Comprar 2–3 dominios similares (~$10/año c/u):

- `devlop-web.com`, `getdevlop.com`, `devlopstudio.com` (o similares disponibles)
- Configurar **redirect 301** de cada uno hacia devlop.it (así el dominio "existe" si alguien lo visita).

## 2. Buzones

- **Google Workspace** (o Microsoft 365): 2–3 buzones por dominio → 6–9 buzones en total.
  - `dani@devlop-web.com`, `hola@devlop-web.com`, etc. — usar nombre de persona real, no "info@".
- Costo: ~$6/buzón/mes → ~$40–55/mes total. Es el gasto más rentable de toda la campaña.
- Foto de perfil real en cada cuenta (las cuentas sin avatar disparan filtros).

## 3. DNS: SPF, DKIM y DMARC en CADA dominio de envío

```
# SPF (TXT en @)
v=spf1 include:_spf.google.com ~all

# DKIM: generar en Google Admin → Apps → Gmail → Autenticar email
#       y publicar el TXT en google._domainkey

# DMARC (TXT en _dmarc)
v=DMARC1; p=quarantine; rua=mailto:dmarc@devlop-web.com; pct=100
```

Verificar con https://www.mail-tester.com (objetivo: 10/10) y `dig TXT _dmarc.dominio.com` antes de enviar nada.

## 4. Warm-up (días 1–14, NO saltear)

Buzones nuevos que envían 100 emails el día 1 van directo a spam para siempre.

- Activar warm-up automático: **Instantly.ai** o **Smartlead** (~$37–97/mes, incluyen warm-up + envío + rotación de buzones) o **Mailwarm/Warmup Inbox** si se envía con `send_campaign.py`.
- Cronograma manual si no se usa herramienta: día 1–3: 5/día · día 4–7: 10/día · semana 2: 20/día · semana 3: 30–40/día (tope por buzón).
- **Mantener el warm-up activo durante toda la campaña** (en segundo plano, ~20% del volumen).

## 5. Límites de envío en régimen (desde día 15)

| Concepto | Límite |
|---|---|
| Por buzón/día | 30–40 cold + follow-ups |
| Por dominio/día | 90–120 |
| Total con 3 dominios | ~150 nuevos + follow-ups/día |
| Intervalo entre envíos | 2–5 min aleatorio (send_campaign.py lo hace) |
| Horario | 9:00–18:00 hora del destinatario, L–V |

## 6. Higiene de lista y contenido

- **Verificar emails antes de enviar**: MillionVerifier/NeverBounce (~$0,003/email). Bounce rate >3% = dominio marcado. `send_campaign.py` excluye los no verificados si la columna `email_verificado` no es `ok`.
- **Texto plano** (o HTML mínimo), sin imágenes, sin adjuntos, **máximo 1 link** (y en toques 1–2, idealmente ninguno: pedir respuesta, no clic).
- Evitar palabras spam: gratis!!!, 100% garantizado, oferta limitada, GANA, $$$.
- Variar contenido entre envíos (el spintax/personalización de `personalize.py` ayuda — Gmail agrupa mensajes idénticos).
- **List-Unsubscribe header** + línea de baja en el pie (send_campaign.py lo añade automático).

## 7. Monitoreo semanal

- Bounce rate <3%, tasa de spam-report ~0, respuestas >2%.
- Google Postmaster Tools (gratis) para reputación de dominio/IP.
- Si un buzón cae en spam: pausarlo 2 semanas y dejar solo warm-up; el resto sigue.

## Resumen de inversión

| Ítem | Costo |
|---|---|
| 3 dominios | ~$30/año |
| 6–9 buzones Workspace | ~$40–55/mes |
| Warm-up/envío (Instantly o similar) | ~$37–97/mes |
| Verificación de emails (10k) | ~$30 una vez |
| Google Places API | $200 crédito gratis/mes (alcanza) |
| **Total** | **~$110–190/mes** |

Con 100 clientes × $30–60/mes de MRR, la campaña se paga sola ~30 veces.
