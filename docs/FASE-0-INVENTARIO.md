# Fase 0 · Inventario (12/10/2026)

Generado con `python -I scripts/inventario_fase0.py`. Datos completos en `docs/inventario-urls.csv`, `inventario-enlaces-rotos.csv` e `inventario-activos.csv`. Solo lectura: no se modificó el sitio.

## Hallazgos medidos

| Dato | Resultado |
|---|---|
| Páginas HTML públicas (sin `admin-temas`) | 33 |
| En `sitemap.xml` | 30; faltan `/agent-printer.html`, `/oauth/drive/callback/`, `/vinculacion-exitosa.html` |
| Entradas del sitemap que no existen | 0 |
| Enlaces internos rotos | 0 |
| Con `noindex` | solo `/vinculacion-correcta.html`; `/vinculacion-exitosa.html` y el callback OAuth no lo declaran (revisar antes de tocar) |
| Canonical distinto de la URL | `/oauth/drive/callback/` (sin canonical) y `/vinculacion-exitosa.html` |
| Sin `og:image` | gestion-inventario-avanzada, gestion-multi-deposito, multiples-cajas-pos, politica-privacidad, terminos-condiciones y las 3 de vinculación/OAuth |
| JSON-LD | Home, blog, categoría y rubros combinan `SoftwareApplication` + `Product` + `FAQPage` (el plan pide unificar). Blog repite SoftwareApplication/Product dentro de cada artículo |
| `/casos-uso-distribuidora-belleza.html` | 0 enlaces entrantes desde el resto del sitio |
| Activo más pesado | `img/adestock_run.gif`, 17,5 MiB; referenciado en index, versiones, gestion-inventario-avanzada, gestion-multi-deposito, multiples-cajas-pos y casos-uso-distribuidora-belleza |
| GA4 `G-W01VQ5GZND` | presente en 16 HTML (recepción de eventos sin verificar) |
| Tutoriales actuales | `tutoriales.html` + `tutoriales/chapters/*.json` (16 capítulos t1–t16 + index) cargados por `render-tutorials.js` |
| Manuales públicos | `manuales/funcional/` (16 MD) y `manuales/changelog/2026/` (12 archivos), bajo `Allow` en robots |
| Idiomas | `translations/{es,en,pt}.js` aplicados por `i18n.js` sobre la misma URL |

Nota del script: la home figura con 0 enlaces entrantes por cómo normaliza la ruta `/`; no es un dato real.

## Hosting (dependencia abierta)

Evidencia: `CNAME` = `adestock.com.ar`, remoto `github.com/adema-websites/adestock`, no hay `.github/`, y `_headers` usa sintaxis de Netlify/Cloudflare Pages. **Es probable GitHub Pages**, que ignora `_headers` y `_redirects`, pero no está confirmado. Decisión que necesita al responsable del negocio: dónde se sirve producción hoy. De eso depende cómo se hacen las redirecciones (Fase 7) y si los `Content-Type`/`Content-Disposition` de `/api/temas-revista/` se están aplicando realmente.

### Actualización: hosting verificado con `curl` (12/10/2026)

- `https://adestock.com.ar/` → `Server: GitHub.com` (Fastly). **Producción pública sigue en GitHub Pages**; `www` hace 301 a la raíz, `/sistema-de-stock` hace 301 a `/sistema-de-stock/`, una ruta inexistente da 404 real.
- `https://adestock.ademasistemas.com/` → Cloudflare, servido desde **Coolify** (app `adestock-landing`, build pack Dockerfile, dominio `adestock.ademasistemas.com`, "Allow www & non-www"). Es un segundo despliegue del mismo contenido.
- `https://adestock.com.ar/api/temas-revista/index.json` da **404** en producción: la API de temas (carpeta sin comitear) todavía no está publicada en ningún lado del dominio principal.
- En el repo no hay `Dockerfile` ni configuración de servidor. Coolify debe estar tomando otra rama/repositorio o una configuración que no veo.

Consecuencias: (1) hoy hay dos sitios con el mismo HTML; si el de Coolify es indexable compite con el principal, aunque su canonical apunte a `adestock.com.ar` (hay que confirmarlo); (2) `_headers` no se aplica en GitHub Pages; (3) si se migra `adestock.com.ar` a Coolify se gana control de redirecciones 301 y headers (necesarios para las fases 7 y el API firmado), pero hay que cambiar DNS y retirar el `CNAME` de Pages.

## Riesgos detectados para fases siguientes

1. `robots.txt` lista `Allow` por carpeta, pero no incluye `/funciones/` ni `/tutoriales/`; con `Allow: /` general no bloquea, pero conviene simplificarlo en Fase 7.
2. El GIF de 17,5 MiB está en 6 páginas comerciales: principal candidato de LCP; reemplazarlo antes de medir rendimiento.
3. `Disallow: /admin-temas/` en robots no equivale a ocultarlo; en Fase 1 sale del directorio público.
4. `i18n.js` puede sobrescribir el copy nuevo; tratarlo en Fase 6 antes de reescribir la home.

## Pendiente para cerrar Fase 0

- [ ] Confirmar hosting de producción.
- [ ] Exportar Search Console (28 y 90 días) y GA4; sin acceso, registrar la limitación y proceder con cautela en redirecciones.
- [ ] Completar `data/migracion-urls.csv` con destino/decisión por URL (las 33 filas del inventario son la base).
- [ ] Backup recuperable: etiqueta Git `pre-renovacion-2026-10` una vez comiteado el estado actual (hay cambios sin comitear en `.gitignore`, `_headers`, `robots.txt`, `sitemap.xml` y carpetas nuevas `admin-temas/`, `api/`, `temas-revistas/`).
- [ ] QA visual individual de las 266 imágenes (se hace por guía en Fase 3–5).
