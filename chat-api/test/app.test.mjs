import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { crearApp, leerConfig } from '../src/app.mjs';

const ORIGEN = 'https://adestock.com.ar';
const indice = {
  sinonimos: { foto: 'boleta compra' },
  fragmentos: [
    { id: 'a#1', tutorial_id: 'cargar-compras-con-foto-ia', url: '/tutoriales/cargar-compras-con-foto-ia/#paso-1', title: 'Cómo cargar una compra con foto e IA', heading: 'Subí la foto', text: 'Sacale una foto a la boleta y subila. El sistema lee los renglones y sugiere los productos.', keywords: 'boleta factura foto', role: ['dueno'], surface: ['panel'] },
    { id: 'b#1', tutorial_id: 'contar-stock', url: '/tutoriales/contar-stock/', title: 'Cómo contar el stock', heading: 'Conteo', text: 'Elegí el depósito y cargá lo que contaste.', keywords: 'conteo', role: ['dueno'], surface: ['panel'] },
  ],
};

let dir;
before(() => { dir = mkdtempSync(join(tmpdir(), 'chat-')); });
after(() => rmSync(dir, { recursive: true, force: true }));

function gemini({ texto = 'Subí la foto de la boleta y revisá los renglones.', entrada = 1000, salida = 100, estado = 200 } = {}) {
  const llamadas = [];
  const fn = async (url, init) => {
    llamadas.push({ url: String(url), init });
    if (estado !== 200) return { ok: false, status: estado, json: async () => ({}) };
    return { ok: true, status: 200, json: async () => ({ candidates: [{ content: { parts: [{ text: texto }] } }], usageMetadata: { promptTokenCount: entrada, candidatesTokenCount: salida } }) };
  };
  fn.llamadas = llamadas;
  return fn;
}

async function levantar(env, fetchImpl) {
  const config = leerConfig({ GEMINI_API_KEY: 'k', DATA_DIR: mkdtempSync(join(dir, 'd-')), ...env });
  const app = crearApp({ config, fetchImpl, indiceInicial: indice });
  await new Promise((r) => app.servidor.listen(0, r));
  const base = `http://127.0.0.1:${app.servidor.address().port}`;
  const post = (body, headers = {}) =>
    fetch(base + '/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: ORIGEN, ...headers }, body: JSON.stringify(body) });
  return { app, base, post, cerrar: () => app.detener() };
}

test('responde con contexto del tutorial y devuelve fuentes', async () => {
  const f = gemini();
  const s = await levantar({}, f);
  const r = await s.post({ message: 'cómo cargo una factura con la cámara' });
  const d = await r.json();
  assert.equal(r.status, 200);
  assert.match(d.answer, /boleta/);
  assert.equal(d.sources[0].url, '/tutoriales/cargar-compras-con-foto-ia/#paso-1');
  const body = JSON.parse(f.llamadas[0].init.body);
  assert.match(body.contents[0].parts[0].text, /Sacale una foto a la boleta/);
  assert.equal(f.llamadas[0].init.headers['x-goog-api-key'], 'k');
  assert.match(f.llamadas[0].url, /gemini-2\.5-flash:generateContent/);
  s.cerrar();
});

test('rechaza origen no permitido y llamadas sin Origin', async () => {
  const s = await levantar({}, gemini());
  assert.equal((await s.post({ message: 'hola' }, { Origin: 'https://otro.com' })).status, 403);
  const sin = await fetch(s.base + '/api/chat', { method: 'POST', body: '{"message":"hola"}' });
  assert.equal(sin.status, 403);
  s.cerrar();
});

test('valida el mensaje', async () => {
  const s = await levantar({ MAX_MESSAGE_CHARS: '20' }, gemini());
  assert.equal((await s.post({ message: '   ' })).status, 400);
  assert.equal((await s.post({ message: 'x'.repeat(21) })).status, 400);
  s.cerrar();
});

test('al llegar al tope mensual deja de llamar a Gemini', async () => {
  const f = gemini({ entrada: 1_000_000, salida: 1_000_000 }); // ~USD 2,80 por consulta con precios por defecto
  const s = await levantar({ MONTHLY_BUDGET_USD: '5', RATE_PER_MIN: '50' }, f);
  const a = await (await s.post({ message: 'foto de factura' })).json();
  assert.equal(a.limited, false);
  await s.post({ message: 'foto de factura' }); // segunda: acumula ~5,6 > 5
  const c = await (await s.post({ message: 'foto de factura' })).json();
  assert.equal(c.limited, true);
  assert.match(c.answer, /WhatsApp/);
  assert.equal(f.llamadas.length, 2);
  s.cerrar();
});

test('limita por IP y por minuto', async () => {
  const f = gemini();
  const s = await levantar({ RATE_PER_MIN: '2' }, f);
  assert.equal((await s.post({ message: 'uno' })).status, 200);
  assert.equal((await s.post({ message: 'dos' })).status, 200);
  const t = await s.post({ message: 'tres' });
  assert.equal(t.status, 429);
  assert.equal((await t.json()).limited, true);
  assert.equal(f.llamadas.length, 2);
  s.cerrar();
});

test('si Gemini falla, responde con aviso y no cobra', async () => {
  const s = await levantar({}, gemini({ estado: 500 }));
  const d = await (await s.post({ message: 'foto de factura' })).json();
  assert.equal(d.limited, true);
  assert.equal(s.app.presupuesto.gastado(), 0);
  s.cerrar();
});

test('sin API key avisa que no está disponible', async () => {
  const s = await levantar({ GEMINI_API_KEY: '' }, gemini());
  const r = await s.post({ message: 'hola' });
  assert.equal(r.status, 503);
  s.cerrar();
});

test('healthz informa gasto y tope sin exponer la clave', async () => {
  const s = await levantar({}, gemini());
  const t = await (await fetch(s.base + '/healthz')).text();
  assert.match(t, /limiteUsd/);
  assert.doesNotMatch(t, /"k"/);
  s.cerrar();
});
