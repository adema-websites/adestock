# Renovación visual 3.0: decisiones y pendientes

Estado: prototipo de la home funcionando en la rama `renovacion`. Versión del producto en el código: **2.5.3**. La web no anuncia "3.0" hasta que salga.

## Dirección

**"Como la app del dueño"** (dirección A). Claro y cálido, tarjetas grandes y redondeadas, tipografía firme (Geist), capturas reales del producto y un solo acento (turquesa de la marca, `#0b7285`, texto blanco con contraste >= 5,5:1). Modo oscuro automático. Botones siempre en pastilla, tarjetas a 22 px, campos a 12 px.

Referencias de diseño: `src/styles/marca.css` (tokens), `src/layouts/Sitio.astro`, `src/components/Site*.astro`.

## Home (`src/pages/index.astro`)

| Sección | Qué muestra | Recurso |
|---|---|---|
| Hero | Promesa, "Probar ADEstock" y "Ver cómo funciona" (abre video) | captura de revista + app del dueño |
| ¿Qué querés hacer primero? | 5 tareas; apuntan a guías si existen, si no al índice vigente | enlaces |
| Revistas | Narración con scroll: 3 pasos que cambian la captura fija | capturas limpias + `video/revista-flujo.webm` |
| Compras con foto | Boleta, resumen con totales, comparación de proveedores | foto de boleta de demo, resumen, app |
| App del dueño | Carril horizontal de 5 pantallas | capturas de la PWA |
| Circuito diario | Bento de 5 celdas (POS, caja, stock, depósitos, cuentas) | solo texto: faltan capturas limpias |
| Para tu negocio | 5 rubros | enlaces existentes |
| Preguntas | 6 preguntas, mismas que el JSON-LD | texto |
| Cierre | CTA a demo y precios | texto |

Movimiento: entradas por scroll con `IntersectionObserver`, narración de revistas sin librerías, transiciones entre páginas con `ClientRouter` de Astro. No hay `scroll` listeners ni GSAP. Todo se apaga con `prefers-reduced-motion`.

## Contenido que se mantuvo y lo que se quitó

- Se mantuvo: FAQ (AFIP, multiempresa, demo de 3 días), navegación a rubros, GA4 `G-W01VQ5GZND`, canonical y `llms.txt`.
- Se quitó de la home: "100 USD pago único" (contradecía `precios.html`, que hoy muestra nube $60.000 + IVA/mes y licencias locales), la versión "v2.3.3" y el modal con credenciales de demo (la demo se pide desde `/descargar-demo.html`).
- La home anterior queda en `docs/legacy/home-2026-10-12.html`.

## Chat "Preguntale a ADEstock"

Widget (`src/components/Chat.astro`) + servicio (`chat-api/`). Detalle y despliegue en `chat-api/README.md`. Sin `PUBLIC_CHAT_URL` el widget responde con el buscador local (extracto real del tutorial y enlace), así que sirve aun sin IA.

## Pendiente antes de publicar

- [x] Demo sembrada (solo base de demo): 45 fotos ilustrativas de producto (packshots generados, no son fotos reales) y dos compras confirmadas de los mismos 5 productos a dos proveedores. Recapturadas la revista, la app del dueño (6 pantallas, incluida "Comparar proveedores": $9.480 de más, +5,9 %) y el POS (`scripts/web-capturas/`).
- [ ] Reemplazar los packshots ilustrativos por fotos reales de producto antes de usar la revista como prueba de resultado.
- [ ] Capturas limpias de caja y de conteo de stock; hoy esas celdas del bento son solo texto. El POS de la captura muestra botones de presupuesto: rearmar el carrito desde una venta nueva.
- [ ] Video corto de compras con foto y de la app del dueño; convertir a MP4 (no hay ffmpeg en esta PC).
- [ ] Revisión de copy con alguien del rubro; en particular "en pocos clics" y el mensaje de ahorro de tiempo, que no están medidos.
- [ ] Probar la home en Safari/iOS y con lector de pantalla; medir LCP/INP/CLS en el despliegue.
- [ ] Migrar `Base.astro` (tutoriales) y las páginas SEO de `public/` al sistema visual nuevo.
- [ ] Conectar el chat real (clave de Google en Coolify) y probar contra la API.
- [ ] SEO: el título y la descripción de la home se mantuvieron; el H1 cambió a "Vendé y controlá el stock de tu comercio". Revisar en Search Console tras publicar.
