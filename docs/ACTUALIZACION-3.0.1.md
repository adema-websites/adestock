# Actualización a ADEstock 3.0.1 y Agent Printer 1.0.7

Fecha: 12/10/2026. Estado en la rama `renovacion`.

## Hecho

| Qué | Detalle |
|---|---|
| Agent Printer 1.0.7 | `public/agent-printer.html`: botón principal, historial (1.0.7 y 1.0.5) y SHA-256 real tomado del `.sha256` del release. Verificado que el `.exe` y el `.sha256` responden 200 |
| Tutoriales 34-38 | Armado de pedidos, notas de crédito y débito, licencia, respaldos y agente de impresión: importados con sus capturas |
| Tutoriales 02-33 | Reimportados: 25 cambiaron en el origen (texto y capturas). Descripciones reescritas a mano |
| Enlaces entre guías | Estaban rotos (`12-turno-de-caja….md`). El importador ahora los convierte a `/tutoriales/<slug>/` |
| Ayuda general | `/ayuda/que-es-adestock/`, `/ayuda/conceptos-clave/`, `/ayuda/preguntas-frecuentes/` (desde 00-inicio, 03-conceptos, 05-faq) |
| Buscador y chat | Indexan tutoriales y ayuda; la FAQ queda fuera porque repite los "Problemas frecuentes" de cada guía y tapaba a la guía correcta |
| `llms.txt` | Ahora se genera en el build con lo publicado; la documentación 2.x queda separada como "puede estar desactualizada" |
| Tarjetas sociales | 41 tarjetas (una por guía) |
| Verificador de enlaces | `node scripts/verificar_enlaces.mjs` revisa enlaces y anclas de `dist/` |

## Pendiente de tu parte

1. **Link del instalador 3.0.1.** `https://github.com/adema-websites/adestock/releases/download/ADEstock-desktop-3.0.1v/Adestock_Installer_v3.0.1.exe` hoy da 404. Cuando exista:
   `node scripts/aplicar_instalador.mjs <URL>` actualiza demo, casos de uso y novedades, y deja 2.3.3 como release anterior.
2. **Revisión y publicación de las guías.** Hoy todas están en borrador (`noindex`, no se generan en producción). Cuando decidas:
   `node scripts/publicar_guias.mjs --revisor "Tu nombre" --todas` (o una lista de slugs). Marca `reviewed_at` con la fecha de hoy.
3. **Guías a revisar antes de publicar:** `usar-app-del-dueno`, `consultar-reportes-y-exportar`, `controlar-turnos-caja-panel` y `billeteras-y-cuentas` declaran en su origen que se verificaron contra la **2.5.3**, no la 3.x (la app del dueño ganó Proveedores y Comparar proveedores).
4. **Versión de producto declarada:** 33 guías heredan `3.0.0` del README de inicio (el origen no trae versión propia); las dos de Excel de la web quedan en `3.0.1` porque el código del importador no cambió desde que se verificó.

## Pendiente conocido

- La captura del instalador del Agent Printer no existe (lo dice el propio tutorial 38).
- `tutoriales.html` (página vieja) conserva anclas `#t1-onboarding…` que ya no existen: se reemplaza por una página puente al publicar el centro nuevo.
- Los manuales 2.x en `/manuales/` siguen siendo públicos.
