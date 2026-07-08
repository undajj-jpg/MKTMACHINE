# 02 — Estrategia de adquisición

## Principio central

dev.lop vende un **servicio productizado de bajo ticket con suscripción**. Eso define toda la estrategia:

- **No** vendemos "desarrollo de software" (venta consultiva, ciclos largos). Vendemos "tu web lista, con todo incluido, por menos de lo que cuesta un café al día".
- El cierre no necesita reuniones largas: cotizador de 2 minutos o llamada de 15. El funnel debe empujar a esos dos destinos.
- Con ticket bajo, el volumen manda: el juego es contactar mucho, personalizar lo justo y responder rápido.

## Los 4 ICPs (perfiles de cliente ideal), en orden de prioridad

### ICP-1: Negocio local SIN página web (60% del esfuerzo)

- **Quiénes**: restaurantes, clínicas dentales/estéticas, gimnasios, talleres, peluquerías, estudios jurídicos/contables, inmobiliarias pequeñas. Tienen Google Maps y/o Instagram pero **no web propia** (o el campo "sitio web" de su ficha apunta a Facebook/Instagram/Linktree).
- **Dolor**: pierden clientes que los buscan en Google; dependen de plataformas que no controlan; se ven menos profesionales que la competencia.
- **Cómo encontrarlos**: `find_leads.py` con Google Places API — busca por rubro+ciudad y filtra los que no tienen `websiteUri` o cuyo "sitio" es una red social. Es un lead hipercalificado: sabemos con certeza que no tienen web.
- **Oferta**: Presencia Web Simple + plan Starter/Growth. Mensaje: *"Tu competencia [nombre real] aparece en Google con web propia y tú no. Te la dejamos lista en días, desde $29/mes con todo incluido."*
- **Canal**: WhatsApp/teléfono de la ficha de Google + email si se encuentra + visita a su Instagram.

### ICP-2: Negocio con web mala u obsoleta (20%)

- **Quiénes**: mismos rubros pero con web que no es responsive, sin HTTPS, hecha en Wix/builder viejo, lenta, o sin actualizar hace años.
- **Cómo encontrarlos**: `find_leads.py` + `enrich_leads.py` — audita cada web y puntúa señales (sin viewport, sin SSL, copyright viejo, generadores obsoletos).
- **Oferta**: rediseño con migración incluida + plan mensual. Mensaje: el **audit personalizado** — *"Entré a [suweb.com] desde el móvil y [problema concreto]. Te preparé 3 mejoras rápidas…"*. Este ángulo tiene las mejores tasas de respuesta del cold email (es imposible de ignorar porque habla de SU web).
- **Canal**: email (tienen email en su web) + WhatsApp.

### ICP-3: Vendedores de Instagram/marketplace sin tienda propia (10%)

- **Quiénes**: marcas pequeñas que venden por DM de Instagram, WhatsApp o Mercado Libre/marketplace, sin e-commerce propio.
- **Dolor**: comisiones de marketplace, ventas manuales por DM, sin catálogo con pagos.
- **Oferta**: E-commerce con pasarela de pagos (Stripe/MercadoPago) + plan mensual. Mensaje: *"Cada venta por DM que se te escapa a las 11pm es una venta que una tienda online hubiera cerrado sola."*
- **Canal**: DM de Instagram + WhatsApp.

### ICP-4: Founders no técnicos / agencias que necesitan MVP o automatización (10%)

- **Quiénes**: emprendedores con idea de SaaS sin CTO; agencias/consultoras ahogadas en procesos manuales.
- **Oferta**: MVP desde $399 con precio fijo, o Automatización con IA desde $149. Mensaje: *"Software a medida con precio fijo: sabes exactamente cuánto pagas y cuándo se entrega."*
- **Canal**: LinkedIn (búsqueda por "founder", "CEO" en startups pequeñas) + comunidades (grupos de emprendedores, Slack/Discord locales).
- **Nota**: ticket más alto, ciclo más largo — es el que sube el promedio de MRR, no el que llena el contador de 100.

## Los 3 ángulos de mensaje que funcionan (y el que no)

1. **La ausencia observada** (ICP-1): "Busqué [negocio] en Google y no encontré tu web — tu ficha manda a Instagram". Concreto, verificable, personal.
2. **El audit gratuito** (ICP-2): 2–3 problemas reales de su web + oferta de arreglarlo. Da valor antes de pedir nada.
3. **El costo de oportunidad** (ICP-3/4): cuánto pierde cada mes sin el activo (ventas nocturnas, comisiones, horas manuales).
4. ❌ **Lo que NO hacer**: "Somos una agencia de desarrollo con X años de experiencia…" — nadie responde a quién eres; responden a qué viste de ELLOS.

## Estructura del funnel

```
Lead (lista) → Toque 1 (email/WA personalizado)
            → Toque 2 (+3 días: bump corto)
            → Toque 3 (+4 días: valor nuevo — mockup/audit/caso)
            → Toque 4 (+5 días: ruptura, "cierro tu carpeta")
Respuesta → Calificar en el hilo → Cotizador (link) o Llamada 15 min → Cierre → Onboarding portal
```

- **Secuencias completas**: `playbooks/emails.md` y `playbooks/whatsapp-linkedin.md`.
- **El mockup vendedor** (arma secreta para ICP-1/2): antes del toque 3, generar con Lovable/IA un borrador de home para el negocio y mandar screenshot: *"Te hice esto en un rato para que veas cómo se vería"*. Costo: minutos. Efecto en cierre: enorme, porque el lead ya se ve dentro del producto.

## Metas de actividad diaria (desde día 15, post warm-up)

| Actividad | Diario | Semanal |
|---|---|---|
| Emails nuevos (toque 1) | 60–80 | ~400 |
| Follow-ups automáticos | 50–70 | ~350 |
| WhatsApp nuevos | 20–30 | ~150 |
| Invitaciones LinkedIn | 15–20 | ~90 |
| Respuestas atendidas | todas, <2h | — |
| Llamadas de 15 min | 2–4 | 15–20 |
| **Cierres** | **1–1,5** | **7–10** |

## Palancas si el ritmo no alcanza (revisar cada viernes con `track.py stats`)

- Tasa de respuesta <2% → cambiar ángulo/asunto (A/B en playbooks), revisar entregabilidad (docs/03).
- Respuestas sí, cierres no → problema de oferta o velocidad: añadir garantía ("si no te gusta el diseño, no pagas"), mandar el mockup antes.
- Todo bien pero falta volumen → añadir tercer dominio de envío + más ciudades/rubros en find_leads.
- Desde el día 30: **motor de referidos** — a cada cliente cerrado, ofrecerle 1 mes gratis por cada negocio que refiera y cierre. Con 30+ clientes esto genera 10–15 extra solo.
