# Playbook — Secuencias de cold email

Reglas de todas las secuencias:

- **Texto plano**, 50–120 palabras, 1 sola pregunta, 0–1 links.
- Variables entre `{{llaves}}` — las rellenan `personalize.py` y `send_campaign.py`.
- Cadencia: T1 → +3 días T2 → +4 días T3 → +5 días T4. Si responde, la secuencia se corta (marcar en track.py).
- Firma legal SIEMPRE (se añade automática desde la plantilla base).
- Las versiones `.txt` listas para `send_campaign.py` están en `playbooks/templates/`.

---

## SECUENCIA ICP-1 · Negocio local sin web

### T1 — La ausencia observada

**Asunto (A/B):** `¿la web de {{negocio}}?` · `{{negocio}} en Google`

```
Hola {{nombre}},

{{primera_linea}}

Busqué {{negocio}} en Google y no encontré página web propia — la ficha
lleva a {{red_social}}. Cada persona que te busca y no encuentra web
termina en la competencia que sí la tiene.

Nosotros dejamos webs listas en días, con hosting, cambios y soporte
incluidos desde $29/mes. Sin pagar miles por adelantado.

¿Te muestro cómo se vería la de {{negocio}}? Respondeme "sí" y te mando
una propuesta visual sin compromiso.

{{firma}}
```

### T2 — Bump corto (+3 días)

**Asunto:** (responder en el mismo hilo)

```
Hola {{nombre}}, ¿viste mi mensaje anterior?

Solo para dimensionar: el 76% de la gente mira la web de un negocio
antes de visitarlo o llamar. Sin web, esa primera impresión la decide
tu competencia.

¿Te interesa que te arme una propuesta? Es gratis y sin compromiso.

{{firma}}
```

### T3 — El mockup vendedor (+4 días)

**Asunto:** `te hice un boceto de la web de {{negocio}}`

```
{{nombre}}, me tomé un rato y armé un boceto de cómo podría verse la
web de {{negocio}}: [adjuntar screenshot o link al mockup]

Es solo una primera idea — colores, fotos y textos se ajustan a tu
gusto (los cambios están incluidos en el plan mensual).

Si te gusta, en menos de una semana está online. ¿Lo vemos en una
llamada de 15 minutos? → {{link_agenda}}

{{firma}}
```

### T4 — Ruptura (+5 días)

**Asunto:** (mismo hilo)

```
{{nombre}}, te escribí un par de veces por la web de {{negocio}} y no
quiero ser pesado, así que este es mi último mensaje.

Si en algún momento querés que {{negocio}} aparezca en Google con web
propia, escribime o entrá a devlop.it — el cotizador tarda 2 minutos.

¡Éxitos con el negocio!

{{firma}}
```

---

## SECUENCIA ICP-2 · Web mala u obsoleta

### T1 — El audit personalizado

**Asunto (A/B):** `3 cosas de {{dominio_lead}}` · `entré a tu web desde el móvil`

```
Hola {{nombre}},

Entré a {{dominio_lead}} y encontré algunas cosas que te están
costando clientes:

{{hallazgos}}

Son arreglos que hacemos habitualmente — o directamente una web nueva
con hosting, cambios y soporte incluidos desde $29/mes.

¿Querés que te mande el detalle completo del análisis? Es gratis.

{{firma}}
```

(`{{hallazgos}}` lo genera `enrich_leads.py`: 2–3 bullets concretos, p.ej. "— No se adapta a móvil (60%+ de tus visitas)", "— Sin candado de seguridad (Chrome la marca 'No segura')".)

### T2 — Bump (+3 días)

```
{{nombre}}, ¿llegaste a ver el análisis de {{dominio_lead}}?

Lo más urgente es {{hallazgo_principal}} — es de esas cosas que no se
ven desde adentro pero espantan clientes todos los días.

¿Te mando la propuesta de arreglo?

{{firma}}
```

### T3 — Caso + precio ancla (+4 días)

```
{{nombre}}, te dejo un ejemplo concreto: a {{caso_nombre}} le
renovamos la web el mes pasado — {{caso_resultado}}.

Lo mejor: no pagó un proyecto de miles. Plan mensual desde $29 con
todo incluido, y la web nueva queda online en días. El código es suyo.

¿Vemos la de {{negocio}} en 15 minutos? → {{link_agenda}}

{{firma}}
```

### T4 — Ruptura (+5 días)

```
{{nombre}}, último mensaje de mi parte.

El análisis de {{dominio_lead}} queda hecho — si querés retomarlo en
cualquier momento, respondé este email o entrá a devlop.it.

¡Éxitos!

{{firma}}
```

---

## SECUENCIA ICP-3 · Vende por Instagram/marketplace sin tienda

### T1

**Asunto:** `las ventas que se te escapan por DM`

```
Hola {{nombre}},

Vi {{cuenta_ig}} — buen producto y buena comunidad. Pero me imagino la
cantidad de ventas que se cierran (o se pierden) por DM a cualquier hora.

Con una tienda online propia, el catálogo, los pagos y los envíos se
manejan solos: el cliente compra a las 11 de la noche sin que estés
del otro lado. Pasarela de pagos incluida (Stripe, MercadoPago).

Planes mensuales con todo incluido — sin comisiones por venta.

¿Te muestro cómo se vería la tienda de {{negocio}}?

{{firma}}
```

### T2 (+3 días) — bump 2 líneas. T3 (+4) — mockup de la tienda. T4 (+5) — ruptura.
(Los cuerpos siguen el mismo patrón que ICP-1; adaptar en templates/.)

---

## SECUENCIA ICP-4 · Founder no técnico / automatización

### T1 (vía LinkedIn o email)

**Asunto:** `precio fijo para el MVP de {{proyecto_o_empresa}}`

```
Hola {{nombre}},

Vi que estás construyendo {{proyecto_o_empresa}}. La queja #1 de los
founders no técnicos con las agencias: presupuestos que se estiran y
plazos que nadie cumple.

Nosotros lo hacemos al revés: precio fijo y fecha fija, desde $399.
Sabés exactamente cuánto pagás y cuándo se entrega. MVPs, dashboards,
APIs — y el código es tuyo.

¿Tenés 15 minutos esta semana? Te cotizo en la misma llamada.

{{firma}}
```

Follow-ups: T2 bump (+3), T3 caso de MVP entregado (+4), T4 ruptura (+5).

---

## Reglas de A/B testing

1. Testear **una variable por vez** (primero asunto, después primera línea, después CTA).
2. Mínimo 100 envíos por variante antes de declarar ganadora.
3. Métrica de decisión: **tasa de respuesta** (no apertura — sin píxel de tracking somos más entregables).
4. Registrar resultados en `track.py` (campo `variante`).
