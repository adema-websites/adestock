# Línea de base GA4 (14/07/2026 – 11/10/2026, 90 días)

Fuente: exportaciones en `impormes_gcp/`, propiedad ADEstock. Sin Search Console todavía.

## Cifras

| Métrica | Valor |
|---|---|
| Usuarios / nuevos / sesiones | 97 / 91 / 127 |
| Eventos clave (conversiones) | **0** (ningún evento clave configurado o disparado) |
| Eventos `file_download` / `click` | 4 / 6 |
| Sesiones por canal | Direct 81 (16 con interacción), Organic Search 24 (13), AI Assistant 20 (12), Unassigned 2 |
| Fuentes de las sesiones | google 21, chatgpt.com 20, bing 2, yahoo 1 |
| Usuarios por país | Estados Unidos 44, Argentina 32, Alemania 5, Singapur 3, resto ≤2 |
| Idioma | inglés 61, español 34 |

## Lectura (hipótesis, no certezas)

1. **Gran parte del tráfico no parece humano.** 44 usuarios de EE.UU. con 0 sesiones con interacción; 29 de ellos en Council Bluffs (ciudad de un centro de datos) y otros en Ashburn y Columbus. Direct y el idioma inglés tienen la misma firma. Eso infla "Direct" (81 sesiones, 20 % de interacción). Hay que filtrar tráfico de bots/internos antes de comparar nada. Los datos de Argentina (32 usuarios, 56 % de interacción) son la mejor aproximación al público real.
2. **El volumen es muy bajo** (~1 sesión por día). Las métricas porcentuales del plan (CTR, tasa de cero resultados, etc.) no serán estables al principio; medir en conteos absolutos y por mes.
3. **ChatGPT envía tanto tráfico como Google** (20 vs 21 sesiones) y con mejor interacción (60 % vs 54 %). Respalda mantener `llms.txt`, robots abierto a esos agentes y contenido citable (tutoriales en HTML).
4. **Las páginas SEO no aparecen entre las vistas**: no hay vistas de `/sistema-de-stock/`, `/control-de-stock/`, rubros ni blog. Casi todo entra por la home (`/` 97 + `/index.html` 15). `/tutoriales.html` tuvo 2 vistas. Hay dos URLs para la home en GA4, una señal de que hace falta redirección o canonical consistente de `/index.html`.
5. **Dónde hay interés real**: `/precios.html` (145 s de interacción media por usuario) y `/agent-printer.html` (184 s). Una persona de México estuvo 677 s.
6. **No se mide la intención comercial**: no hay `click_whatsapp`, `generate_lead` ni `trial_start`; solo `file_download` (4). Esto confirma que el plan de eventos (sección 17) es prioritario.

## Qué cambia en el plan

- Línea de base de 28 días y de 90 días: la de 90 días queda registrada aquí; falta la de 28 días y Search Console.
- Primer objetivo medible: **configurar eventos de contacto/descarga y marcar `generate_lead`/`click_whatsapp` como eventos clave**, y definir un filtro de tráfico interno y de bots en GA4.
- La meta "tutoriales P0 accesibles y cero enlaces rotos" se mantiene; las metas de tráfico se fijan sobre Argentina y el canal orgánico + IA, no sobre el total.
