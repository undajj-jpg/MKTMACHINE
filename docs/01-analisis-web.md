# 01 — Análisis de devlop.it

Auditoría técnica y de conversión realizada el 2026-07-08. La landing es el destino de todo el tráfico de la campaña: cada punto débil aquí multiplica el costo de adquisición.

## Qué vende dev.lop (resumen del negocio)

- **Propuesta**: "Tu presencia digital, sin complicaciones. Desde landing pages hasta plataformas complejas a medida. Planes mensuales con cambios incluidos."
- **Tres líneas de servicio**:
  1. **Presencia web** (landing, sitio corporativo, e-commerce, webapp) — desde $49; tiers Simple $99 / Avanzado $169 / Complejo $279
  2. **Aplicación** (SaaS, dashboards, APIs, MVPs) — desde $399, hasta $1.109 en tier complejo
  3. **Automatización** (integraciones + IA) — $149 / $249 / $599
- **Planes mensuales de suscripción**: Starter $29 (3 cambios/mes), Growth $59 (8), Business $99 (15), Pro $199 (ilimitados). Incluyen hosting, soporte y cambios.
- **Diferenciadores reales**: precio fijo conocido de antemano, portal de clientes con seguimiento y solicitudes de cambio, cotizador con IA en 2 minutos, entrega "de la idea a tu web en 5 pasos", el cliente es dueño del código al completar el pago.
- **CTAs**: "Completa el cotizador en 2 minutos. Sin compromiso." y "Agendar llamada de 15 minutos" — perfectos como destino de cold outreach.

**Veredicto para la campaña**: la oferta es MUY vendible en frío. "Web profesional con todo incluido por $29-59/mes, sin pagar miles por adelantado" es un mensaje que un negocio local entiende en 5 segundos. El plan mensual es el gancho, no el proyecto.

## Hallazgos técnicos (arreglar antes del día 8)

### Críticos

1. **Disponibilidad intermitente.** Durante la auditoría el sitio devolvió `503 Service Unavailable` y `connection reset` en varios intentos antes de responder 200. Si un lead hace clic desde un email y ve un error, ese lead se pierde para siempre. **Acción**: configurar monitoreo (UptimeRobot gratis, chequeo cada 5 min) y evaluar mover el hosting del preview de Lovable a un dominio productivo estable (Cloudflare Pages / Vercel delante).

2. **SPA 100% renderizada en cliente (sin SSR/prerender).** El HTML que reciben Google y los previews de WhatsApp/LinkedIn es un `<div id="root"></div>` vacío. Google renderiza JS pero con retraso y menor presupuesto de crawl; los bots de previews de mensajería no ejecutan JS. **Acción**: activar prerendering (Lovable lo soporta vía publicación) o SSG para las rutas públicas. Esto importa porque la campaña comparte el link por WhatsApp constantemente.

3. **og:image apunta al bucket de preview de Lovable** (`pub-...r2.dev/...lovable.app...png`). En WhatsApp/LinkedIn el preview puede verse roto o con branding de terceros. **Acción**: subir una imagen OG propia 1200×630 servida desde devlop.it.

### Importantes

4. **Inconsistencia de email**: en el sitio aparece `hola@devlop.com` pero el dominio es `devlop.it`. Si `devlop.com` no es tuyo, se están perdiendo respuestas. **Acción**: unificar a `hola@devlop.it` en todo el sitio y firmas.

5. **Mezcla de voseo y tuteo** en el copy ("Cuéntanos más de tu proyecto" vs "Decile al asistente cómo se llama"). **Acción**: elegir uno según el mercado objetivo (si es LatAm amplio + España, tuteo neutro es lo más seguro) y unificar.

6. **Clave anónima de Supabase visible en el bundle.** Esto es normal en apps Supabase (la anon key es pública por diseño), pero implica que **toda la seguridad depende de las políticas RLS**. **Acción**: auditar que cada tabla tenga RLS activado y políticas correctas — especialmente `profiles`, cotizaciones y datos de clientes. Un fallo aquí expone datos de clientes.

### Mejoras de conversión (aumentan el retorno de la campaña)

7. **Añadir botón de WhatsApp flotante** — el canal #1 de cierre para PyMEs hispanohablantes. Hoy no hay número de WhatsApp visible.
8. **Publicar la tabla de planes mensuales en la home** (Starter/Growth/Business/Pro con precios). El precio transparente es el argumento de venta central del negocio; hoy hay que pasar por el wizard para verlo.
9. **Casos/portfolio con resultados**: existe la sección "Algunos ejemplos de lo que construimos" — añadir 3–5 casos con nombre del negocio, screenshot y un resultado concreto ("+40% de reservas"). El cold traffic necesita prueba social.
10. **Landing pages por ICP con UTM**: crear `/para-restaurantes`, `/para-clinicas`, `/tiendas-online` (aunque sean la misma landing con hero distinto). Los emails de campaña enlazan a la versión de su rubro → conversión mucho mayor. Trackear todo con UTMs (`?utm_source=coldmail&utm_campaign=icp1`).
11. **Testimonios en el cotizador**: el wizard es el punto de conversión — añadir 1–2 testimonios cortos dentro del flujo reduce el abandono.

## Checklist previo al lanzamiento (semana 1)

- [ ] Monitoreo de uptime activo
- [ ] Prerender/SSG de rutas públicas
- [ ] og:image propia
- [ ] Email unificado hola@devlop.it
- [ ] Botón WhatsApp con número real
- [ ] Tabla de precios de planes visible
- [ ] 3 casos de portfolio publicados
- [ ] UTMs configuradas + analytics revisado
- [ ] Auditoría RLS de Supabase
