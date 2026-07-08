# 04 — Marco legal del cold outreach

Esto no es asesoría legal, es el checklist operativo para hacer outbound B2B de forma defendible. Ante dudas con un mercado concreto, consultar a un abogado local.

## Principios que aplican en todos los mercados

1. **Solo B2B**: contactamos negocios y personas en su rol profesional (email/teléfono publicado por el propio negocio en Google, su web o LinkedIn). Nunca listas compradas de consumidores.
2. **Identidad real**: nombre real, negocio real (dev.lop), sin asuntos engañosos ("RE:" falso, "Factura adjunta" = prohibido).
3. **Opt-out en cada mensaje** y baja inmediata al pedirla. `send_campaign.py` añade la línea de baja y `track.py` mantiene la lista de exclusión — un email marcado `baja` no vuelve a contactarse nunca.
4. **Relevancia**: el mensaje debe estar relacionado con la actividad del destinatario (le escribimos sobre SU web a quien tiene un negocio). Esto es lo que sostiene el "interés legítimo".
5. **Registro**: guardar fuente del dato y fecha (find_leads.py lo registra en la columna `fuente`).

## España / UE — RGPD + LSSI (el marco más estricto)

- Base legal: **interés legítimo (art. 6.1.f RGPD)** para B2B, con matices:
  - Emails corporativos genéricos (info@, hola@negocio.com) → riesgo bajo.
  - Emails de persona identificable (nombre@negocio.com) → siguen siendo datos personales: el mensaje debe ser estrictamente profesional y pertinente al cargo, y hay que poder justificar el balancing test (interés del negocio vs. impacto mínimo en el destinatario).
- La **LSSI (art. 21)** prohíbe comunicaciones comerciales no solicitadas *salvo* relación previa — pero la práctica sancionadora de la AEPD se ha centrado en B2C masivo y listas compradas; el B2B artesanal, relevante, de bajo volumen y con opt-out claro es la zona de práctica estándar del sector. Para minimizar riesgo en España: priorizar WhatsApp/teléfono publicado por el negocio y formularios de contacto, y en email preferir direcciones genéricas del negocio.
- Obligatorio en el pie: quién eres, empresa, cómo obtuviste el contacto ("encontré tu negocio en Google Maps"), y enlace/instrucción de baja.
- Derechos ARCO: si alguien pide saber qué datos tienes o borrarlos, responder en <30 días (con este sistema: buscar en leads.csv/SQLite y borrar).

## Latinoamérica

- **Argentina** (Ley 25.326): permite contacto no solicitado con opt-out ("retiro o bloqueo" art. 27). Cumplimos de sobra.
- **México** (LFPDPPP): datos de contacto laboral tienen régimen flexible; aviso de identidad + opt-out.
- **Chile, Colombia, Perú**: regímenes similares — identidad clara + finalidad + opt-out. La regla de los 5 principios de arriba cubre todos.

## EE.UU. — CAN-SPAM (si se contacta mercado US)

- El cold email B2B es legal con: remitente veraz, asunto no engañoso, dirección postal física en el pie, opt-out funcional procesado en <10 días.

## WhatsApp e Instagram

- **WhatsApp**: usar número business normal, mensajes 1-a-1 personalizados y pocos por día (20–30). No usar herramientas de bulk no oficiales (baneo de número casi seguro + problemas legales). Si el negocio publicó su WhatsApp en Google/su web, contactarlo con una propuesta pertinente es práctica comercial estándar; parar al primer "no me interesa".
- **Instagram DM**: mismo criterio; límites de la plataforma ~20–30 DMs/día en cuenta madura.

## Texto de pie estándar (ya incluido en las plantillas)

```
--
[Nombre] · dev.lop — webs y software con todo incluido · devlop.it
Te escribo porque encontré [tu negocio] en [Google Maps / tu web].
Si prefieres que no te contacte más, responde "baja" y listo.
```
