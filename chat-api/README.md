# chat-api · "Preguntale a ADEstock"

Servicio chico (Node 22, sin framework) que responde preguntas sobre el sistema usando **Gemini** y los tutoriales como única fuente.

```
navegador ──POST /api/chat──▶ chat-api ──▶ índice de tutoriales (el mismo MiniSearch del sitio)
                                   └────▶ Gemini (generateContent) con solo esos extractos
```

## Qué garantiza

- **Solo responde con extractos de tutoriales y hechos comerciales** (`src/prompt.mjs`). Si no alcanza, lo dice y deriva a WhatsApp.
- **Tope de gasto mensual** (`MONTHLY_BUDGET_USD`, por defecto 10): se estima con los tokens que informa Gemini y se persiste en `/data`. Al llegar, deja de llamar al modelo y avisa.
- **Límite por IP**: 6 por minuto y 40 por día (configurable).
- **Solo desde los sitios de ADEstock** (`ALLOWED_ORIGINS`); la clave nunca llega al navegador.
- **No guarda ni loguea las consultas** (solo cuenta gasto y cantidad).
- Si el servicio falla o llega al tope, **el widget del sitio cae al buscador local** sin IA.

## Variables

| Variable | Defecto | Nota |
|---|---|---|
| `GEMINI_API_KEY` | (obligatoria) | Clave de Google AI Studio. Cargarla como *secret* en Coolify |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Verificar el modelo vigente y su tarifa |
| `MONTHLY_BUDGET_USD` | `10` | Tope mensual |
| `PRICE_IN_PER_M` / `PRICE_OUT_PER_M` | `0.30` / `2.50` | USD por millón de tokens. **Valores de referencia: verificar en la tarifa de Google** |
| `ALLOWED_ORIGINS` | adestock.com.ar, www, adestock.ademasistemas.com | Separados por coma |
| `INDEX_URL` | `https://adestock.com.ar/tutoriales/indice.json` | Se refresca cada hora |
| `DATA_DIR` | `/data` | Montar un volumen persistente |
| `RATE_PER_MIN` / `RATE_PER_DAY` | `6` / `40` | Por IP |
| `MAX_OUTPUT_TOKENS` | `450` | Respuestas cortas |
| `RESERVE_USD_PER_REQUEST` | `0.01` | Margen para no pasarse del tope |

## Despliegue en Coolify (segunda aplicación)

1. *New resource* → Public/Private Repository: `adema-websites/adestock`, rama `renovacion` (luego `main`).
2. Build Pack **Dockerfile**, *Base Directory* `/`, *Dockerfile Location* `/chat-api/Dockerfile`, puerto `3000`.
3. Dominio: `https://chat.adestock.com.ar` (el DNS comodín `*` de Cloudflare ya apunta al servidor).
4. *Environment Variables*: `GEMINI_API_KEY` (secret) y las demás si querés cambiar valores.
5. *Persistent Storage*: volumen montado en `/data`.
6. Deploy y probar: `GET https://chat.adestock.com.ar/healthz` debe mostrar `limiteUsd` y `indice: true` tras la primera consulta.
7. En la app **del sitio** agregar la *Build Variable* `PUBLIC_CHAT_URL=https://chat.adestock.com.ar/api/chat` y redeploy.

## Pruebas

```bash
cd chat-api && npm install && npm test   # 8 pruebas con Gemini simulado
```

## Pendiente

- Probar contra la API real de Gemini (las pruebas simulan la respuesta).
- Conversación con memoria (hoy cada pregunta es independiente, para controlar el costo).
- Pasar `PRICE_*` a los valores oficiales y alertar al 80 % del tope.
- Registrar preguntas sin respuesta (anonimizadas) para decidir nuevos tutoriales.
