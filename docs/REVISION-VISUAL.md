# Revisión visual completa (12/10/2026)

Todas las páginas públicas usan ahora el mismo sistema: tokens de `src/styles/marca.css`, layout común `src/layouts/Pagina.astro` (navegación, pie, asistente) y estilos de `src/styles/paginas.css` y `tutoriales.css`. Claro y oscuro automático, una sola tipografía (Geist, autoalojada) y un solo acento.

| Familia | Páginas | Cómo se migró |
|---|---|---|
| Home | `/` | Rediseñada a mano; suma la sección "Cómo funciona" (POS, panel, app del dueño; nube o PC) |
| Páginas comerciales | `precios.html`, `contacto.html`, `descargar-demo.html`, `agent-printer.html`, `versiones.html` | Rehechas a mano con componentes nuevos. Precios y versiones leen `src/data/*.json` |
| SEO | sistema de stock, control de stock/inventarios, software de inventario, 3 rubros, blog (índice y 6 notas) | `scripts/migrar_seo.mjs`: se conserva texto, estructura y JSON-LD; originales en `docs/legacy/paginas/` |
| Casos de uso, gestión, legales | 3 casos de uso, 2 de gestión, POS y cajas, privacidad, términos | `scripts/migrar_inline.mjs`: se conserva el texto y los enlaces; se descartan estilos e íconos viejos |
| Centro de ayuda | `/tutoriales/`, guías, `/ayuda/*`, `tutoriales.html` | `Base.astro` pasó al layout común; `tutoriales.html` se renderiza en HTML y pasa a puente al publicar |
| Tienda de temas | `/temas-revistas/` | Solo el marco visual; el JavaScript y la API firmada no se tocaron |
| Transaccionales | vinculación y callback de Drive | Solo paleta y tipografía; lógica intacta |
| 404 | `/404.html` | Página con el layout común |

## Infraestructura nueva

- `src/lib/post-build.mjs`: genera las URLs `.html` como archivo (sin redirección) y el `sitemap.xml` escaneando el resultado real (excluye `noindex`, exige canonical propio).
- `scripts/verificar_enlaces.mjs`: 2.952 enlaces y anclas revisados, 0 rotos.
- Se eliminaron del sitio publicado `styles.css`, `styles-modern.css`, `seo-pages.css`, `site-nav.js`, `i18n.js`, `translations/` y el GIF de 17,5 MiB.

## Pendiente conocido

- Los textos migrados mezclan tuteo ("Descubre", "Ingresa") con voseo; no se reescribieron.
- Los casos de uso conservan afirmaciones heredadas (vencimientos y lotes, FIFO, "funciona sin conexión") que no se reverificaron contra 3.0.1.
- El selector de idioma (en/pt) se retiró: ya no hay traducciones automáticas sobre la misma URL, como pedía el plan.
- Pendiente medir rendimiento real (LCP/INP/CLS) y probar en Safari/iOS.
