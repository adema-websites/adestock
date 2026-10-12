# Fase 2 · Base de ayuda (en curso)

## Hecho

- `scripts/importar_tutoriales.mjs` importa los 32 tutoriales de `documentacion/01-manual-usuario/` a `src/content/tutoriales/*.md` como **borradores** (`status: draft`), con `source_path`, `source_hash` (SHA-256 del origen), versión y fecha de verificación. Es idempotente: reimportar actualiza el texto y la huella, pero conserva `status`, `reviewed_at`, `product_version`, `related`, `social_image`, `title` y `description` ya editados.
- `src/data/tutoriales-mapa.json`: slug, título en forma de acción, categoría, prioridad P0–P2, roles, superficie y sinónimos de los 32. La sección "Qué pasa por detrás" se conserva hasta la revisión editorial.
- Esquema de contenido (`src/content.config.ts`): **un tutorial `published` no compila** sin `reviewed_at`, `product_version` distinta de `pendiente-verificar`, `social_image`, requisitos y permiso. Los `related` inexistentes también rompen el build. Probado.
- Páginas: `/tutoriales/` (tareas más buscadas + todas las guías), `/tutoriales/empezar/` (ruta inicial), `/tutoriales/categorias/{cat}/` (solo con contenido), `/tutoriales/{slug}/`. HTML completo sin JS, breadcrumbs, `TechArticle` + `BreadcrumbList` (el `TechArticle` solo en publicados), canonical, Open Graph, `noindex` en borradores.
- Capturas: `figure` + `figcaption`, WebP generado por Astro, `width`/`height`, lazy; ampliación con teclado (clic/Enter, Esc). Probado a 390 px sin scroll horizontal.
- Borradores: `INCLUDE_DRAFTS=1` (staging) o `npm run dev` los publican con `noindex`. En producción (por defecto) no se generan; `/tutoriales/` y `/tutoriales/empezar/` quedan vacías y con `noindex` hasta publicar la primera guía.

- Buscador local: MiniSearch + diccionario editorial de sinónimos (`src/data/sinonimos.json`). Índice generado en el build (`/tutoriales/indice.json`, 236 fragmentos, ~65 KiB gzip; presupuesto 300 KiB). Resultados agrupados por guía con hasta 3 pasos con enlace directo al encabezado, filtros por rol y superficie, estado vacío con salidas útiles. `/tutoriales/buscar/` es `noindex`.
- Banco de 30 consultas (`src/data/consultas-prueba.json`) y `scripts/probar_buscador.mjs`. Resultado actual: guía correcta entre las 3 primeras 30/30, en 1.º lugar 29/30, críticas 10/10. **Salvedad:** las consultas las redactó el equipo de desarrollo y los sinónimos se ajustaron mirando sus fallos, así que el número es optimista. Falta validarlo con consultas reales (GA4 `search`/Search Console) y con personas del rubro. La respuesta visible <200 ms no está medida.
- Sin desambiguación "¿importar productos o cargar existencias?" hasta que existan esas guías.

## Pendiente de esta fase

- [ ] Los WebP usan la calidad por defecto de Astro (con pérdida): comparar nitidez del texto contra WebP sin pérdida y decidir (plan, sección 16). Sin `srcset` todavía.
- [ ] `description` de los borradores es un recorte automático de "Qué vas a lograr": reescribir al revisar cada guía.
- [ ] Tarjetas sociales 1200×630 por tutorial P0.
- [ ] Sitemap generado (hoy sigue el `sitemap.xml` estático, sin tutoriales).
- [ ] El formulario `contacto.html?tutorial=…` todavía ignora el parámetro.

## Staging

En Coolify, definí la variable `INCLUDE_DRAFTS=1` marcada como *Build Variable* para ver los borradores en `adestock.ademasistemas.com`. Producción no la lleva.
