// Configuración compartida del buscador: la usan la página /tutoriales/buscar/ (navegador) y
// scripts/probar_buscador.mjs (Node), para que el banco de consultas pruebe exactamente lo que ve la gente.

export const normalizar = (s) =>
  s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9ñ\s]/g, ' ');

const STOP = new Set('el la los las un una unos unas de del en y o a que con por para mi me se lo al es si no pero como cual donde'.split(' '));

export const opcionesMiniSearch = {
  idField: 'id',
  fields: ['title', 'heading', 'keywords', 'text'],
  storeFields: ['tutorial_id', 'url', 'title', 'heading', 'text', 'role', 'surface'],
  processTerm: (t) => {
    const n = normalizar(t).trim();
    return n && !STOP.has(n) ? n : null;
  },
  searchOptions: {
    boost: { title: 6, heading: 4, keywords: 3, text: 1 },
    prefix: (term) => term.length >= 4,
    fuzzy: (term) => (term.length >= 6 ? 0.2 : false),
  },
};

export function expandir(consulta, sinonimos) {
  const extra = [];
  for (const palabra of normalizar(consulta).split(/\s+/).filter(Boolean)) {
    if (sinonimos[palabra]) extra.push(sinonimos[palabra]);
  }
  return extra.length ? `${consulta} ${extra.join(' ')}` : consulta;
}

// Busca con AND (todas las palabras); si no hay nada, con OR. Agrupa por tutorial y deja hasta 3 pasos.
export function buscar(ms, consulta, sinonimos, filtro = {}) {
  const q = expandir(consulta, sinonimos);
  const filter = (r) =>
    (!filtro.role || r.role.includes(filtro.role)) && (!filtro.surface || r.surface.includes(filtro.surface));
  let res = ms.search(q, { combineWith: 'AND', filter });
  if (res.length === 0) res = ms.search(q, { combineWith: 'OR', filter });
  const grupos = new Map();
  for (const r of res) {
    let g = grupos.get(r.tutorial_id);
    if (!g) grupos.set(r.tutorial_id, (g = { tutorial_id: r.tutorial_id, title: r.title, score: r.score, pasos: [] }));
    if (g.pasos.length < 3) g.pasos.push(r);
  }
  return [...grupos.values()];
}
