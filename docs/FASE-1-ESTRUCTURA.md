# Fase 1 · Reorganización (rama `renovacion`)

## Estructura

```text
public/            sitio actual, publicado tal cual (URLs intactas). Se irá reemplazando por páginas Astro
src/               layouts, components, content, data, pages (vacío: Fase 2)
tools/admin-temas/ panel Flask de temas (ya NO se publica); escribe en public/api/temas-revista/
deploy/            nginx.conf + cabeceras (sustituye a _headers de GitHub Pages)
Dockerfile         build Astro -> nginx
docs/              plan, inventario, línea base, contrato de temas (fuera del sitio)
scripts/           herramientas (inventario_fase0.py)
CNAME              solo para GitHub Pages; borrar el día del corte de DNS
```

## Por qué una rama

GitHub Pages publica la raíz de `main`. Mientras `adestock.com.ar` siga apuntando a Pages, **`main` no se toca**; la rama `renovacion` se despliega en Coolify y se prueba en `adestock.ademasistemas.com`. Cuando el sitio esté verificado: apuntar el DNS a Coolify, fusionar a `main`, desactivar Pages y borrar `CNAME`.

## Verificado

- `npm run build` genera `dist/` idéntico a `public/` (0 páginas Astro todavía).
- 115 tests del panel de temas pasan tras moverlo (ruta del sitio por defecto: `public/`).
- Inventario de URLs sigue funcionando (`python -I scripts/inventario_fase0.py`, ahora sobre `public/`).

## No verificado (no hay Docker local)

- Build de la imagen y `deploy/nginx.conf`. Comprobar tras el primer deploy en Coolify con `curl -I`:
  `/sistema-de-stock` → 301 a `/sistema-de-stock/`; `/index.html` → 301 a `/`; `/blog/index.html` → 301 a `/blog/`; `/no-existe` → 404;
  `/api/temas-revista/index.json` → `application/json` y 200; `.zip` con `Content-Disposition: attachment`; `/.git/config` → 404;
  `.md` como `text/markdown`.

## Configuración de Coolify

Source: repo `adema-websites/adestock`, **rama `renovacion`**, Build Pack Dockerfile, Dockerfile en `/Dockerfile`, puerto expuesto 80, dominio `adestock.ademasistemas.com`. Para el corte final: dominio `adestock.com.ar` y "Redirect to non-www".
