// Servicio de chat de ADEstock: recupera extractos de los tutoriales (mismo buscador que el sitio) y
// le pide a Gemini que responda solo con eso. Sin dependencias de framework: node:http + fetch.
import { createServer } from 'node:http';
import MiniSearch from 'minisearch';
import { buscar, opcionesMiniSearch } from '../../src/lib/buscador-config.mjs';
import { crearPresupuesto } from './budget.mjs';
import { crearLimitador } from './ratelimit.mjs';
import { armarContexto, systemPrompt } from './prompt.mjs';

const num = (v, d) => (v === undefined || v === '' || Number.isNaN(Number(v)) ? d : Number(v));

export function leerConfig(env = process.env) {
  return {
    port: num(env.PORT, 3000),
    apiKey: env.GEMINI_API_KEY ?? '',
    modelo: env.GEMINI_MODEL || 'gemini-2.5-flash',
    origenes: (env.ALLOWED_ORIGINS || 'https://adestock.com.ar,https://www.adestock.com.ar,https://adestock.ademasistemas.com')
      .split(',').map((s) => s.trim()).filter(Boolean),
    indiceUrl: env.INDEX_URL || 'https://adestock.com.ar/tutoriales/indice.json',
    dataDir: env.DATA_DIR || '/data',
    limiteUsd: num(env.MONTHLY_BUDGET_USD, 10),
    // Valores de referencia en USD por millón de tokens. VERIFICAR contra la tarifa vigente de Google AI.
    precioEntradaPorM: num(env.PRICE_IN_PER_M, 0.30),
    precioSalidaPorM: num(env.PRICE_OUT_PER_M, 2.50),
    maxSalidaTokens: num(env.MAX_OUTPUT_TOKENS, 450),
    maxMensaje: num(env.MAX_MESSAGE_CHARS, 300),
    porMinuto: num(env.RATE_PER_MIN, 6),
    porDia: num(env.RATE_PER_DAY, 40),
    whatsapp: env.WHATSAPP_URL || 'https://wa.me/5491127888995',
    reservaUsd: num(env.RESERVE_USD_PER_REQUEST, 0.01),
  };
}

export function crearApp({ config = leerConfig(), fetchImpl = fetch, indiceInicial = null } = {}) {
  const presupuesto = crearPresupuesto({
    dir: config.dataDir,
    limiteUsd: config.limiteUsd,
    precioEntradaPorM: config.precioEntradaPorM,
    precioSalidaPorM: config.precioSalidaPorM,
  });
  const limitador = crearLimitador({ porMinuto: config.porMinuto, porDia: config.porDia });

  // Índice de tutoriales: se descarga del sitio y se refresca cada hora.
  let ms = null;
  let sinonimos = {};
  let cargadoEn = 0;
  const instalarIndice = (d) => {
    const nuevo = new MiniSearch(opcionesMiniSearch);
    nuevo.addAll(d.fragmentos ?? []);
    ms = nuevo;
    sinonimos = d.sinonimos ?? {};
    cargadoEn = Date.now();
  };
  if (indiceInicial) instalarIndice(indiceInicial);
  async function asegurarIndice() {
    if (ms && Date.now() - cargadoEn < 3_600_000) return;
    try {
      const r = await fetchImpl(config.indiceUrl, { signal: AbortSignal.timeout(5000) });
      if (r.ok) instalarIndice(await r.json());
    } catch { /* se usa el índice anterior o ninguno */ }
  }

  const LIMITADO = 'Por hoy ya respondí muchas consultas. Para que no te quedes sin ayuda, escribinos por WhatsApp y te contestamos.';
  const ERROR = 'No pude responder en este momento. Probá de nuevo en unos minutos o escribinos por WhatsApp.';

  const cors = (req) => {
    const o = req.headers.origin;
    const ok = o && config.origenes.includes(o);
    return ok
      ? { 'Access-Control-Allow-Origin': o, Vary: 'Origin', 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' }
      : { Vary: 'Origin' };
  };
  const enviar = (res, estado, cuerpo, extra = {}) => {
    res.writeHead(estado, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...extra });
    res.end(JSON.stringify(cuerpo));
  };
  const ipDe = (req) =>
    req.headers['cf-connecting-ip'] || String(req.headers['x-forwarded-for'] ?? '').split(',')[0].trim() || req.socket.remoteAddress || 'desconocida';

  async function leerCuerpo(req, max = 4096) {
    let total = 0;
    const partes = [];
    for await (const c of req) {
      total += c.length;
      if (total > max) throw Object.assign(new Error('cuerpo grande'), { estado: 413 });
      partes.push(c);
    }
    return Buffer.concat(partes).toString('utf8');
  }

  async function preguntarAGemini(pregunta, contexto) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(config.modelo)}:generateContent`;
    const r = await fetchImpl(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': config.apiKey },
      signal: AbortSignal.timeout(20_000),
      body: JSON.stringify({
        systemInstruction: { parts: [{ text: systemPrompt({ whatsapp: config.whatsapp }) }] },
        contents: [{ role: 'user', parts: [{ text: `${contexto}\n\nPREGUNTA DEL USUARIO (texto entre comillas triples):\n"""${pregunta}"""` }] }],
        generationConfig: {
          temperature: 0.2,
          maxOutputTokens: config.maxSalidaTokens,
          thinkingConfig: { thinkingBudget: 0 }, // sin razonamiento extendido: más barato y rápido
        },
      }),
    });
    if (!r.ok) throw new Error(`gemini ${r.status}`);
    const d = await r.json();
    const texto = d?.candidates?.[0]?.content?.parts?.map((p) => p.text ?? '').join('').trim() ?? '';
    const u = d?.usageMetadata ?? {};
    return { texto, tokensEntrada: u.promptTokenCount ?? 0, tokensSalida: u.candidatesTokenCount ?? 0 };
  }

  const servidor = createServer(async (req, res) => {
    const url = new URL(req.url ?? '/', 'http://x');
    try {
      if (url.pathname === '/healthz') return enviar(res, 200, { ok: true, ...presupuesto.resumen(), modelo: config.modelo, indice: Boolean(ms) });

      if (url.pathname !== '/api/chat') return enviar(res, 404, { error: 'no encontrado' });
      const h = cors(req);
      if (req.method === 'OPTIONS') { res.writeHead(204, h); return res.end(); }
      if (req.method !== 'POST') return enviar(res, 405, { error: 'método no permitido' }, h);

      // Solo desde los sitios de ADEstock (el navegador manda Origin; las llamadas directas sin Origin se rechazan).
      if (!req.headers.origin || !config.origenes.includes(req.headers.origin)) return enviar(res, 403, { error: 'origen no permitido' }, h);
      if (!config.apiKey) return enviar(res, 503, { answer: ERROR, sources: [], limited: true }, h);

      let datos;
      try { datos = JSON.parse(await leerCuerpo(req)); } catch (e) { return enviar(res, e.estado ?? 400, { error: 'solicitud inválida' }, h); }
      const pregunta = String(datos?.message ?? '').replace(/\s+/g, ' ').trim();
      if (!pregunta) return enviar(res, 400, { error: 'mensaje vacío' }, h);
      if (pregunta.length > config.maxMensaje) return enviar(res, 400, { error: `máximo ${config.maxMensaje} caracteres` }, h);

      if (!limitador.permitir(ipDe(req))) return enviar(res, 429, { answer: LIMITADO, sources: [], limited: true }, h);
      if (presupuesto.agotado(config.reservaUsd)) return enviar(res, 200, { answer: LIMITADO, sources: [], limited: true }, h);

      await asegurarIndice();
      const grupos = ms ? buscar(ms, pregunta, sinonimos).slice(0, 3) : [];
      const fragmentos = grupos.flatMap((g) => g.pasos.slice(0, 2));
      let r;
      try {
        r = await preguntarAGemini(pregunta, armarContexto(fragmentos));
      } catch {
        return enviar(res, 200, { answer: ERROR, sources: [], limited: true }, h);
      }
      presupuesto.registrar({ tokensEntrada: r.tokensEntrada, tokensSalida: r.tokensSalida });
      const fuentes = grupos.map((g) => ({ titulo: g.title, url: g.pasos[0].url }));
      return enviar(res, 200, { answer: r.texto || ERROR, sources: r.texto ? fuentes : [] , limited: !r.texto }, h);
    } catch {
      // Nunca se loguea el contenido de la consulta.
      console.error('error interno en /api/chat');
      return enviar(res, 500, { answer: ERROR, sources: [], limited: true });
    }
  });

  return { servidor, config, presupuesto, detener: () => { limitador.detener(); servidor.close(); } };
}
