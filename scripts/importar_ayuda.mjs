// Importa Empezá acá (00-inicio), Conceptos (03-conceptos) y Preguntas frecuentes (05-faq) a src/content/ayuda.
// Uso:  node scripts/importar_ayuda.mjs [ruta/documentacion]
// Igual que importar_tutoriales: nunca publica; conserva status/revisión/title/description ya editados.
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const DOC = resolve(
  process.argv[2] ??
    [join(ROOT, '..', '..', 'ESCRITORIO', 'adestock', 'documentacion'), join(ROOT, '..', 'documentacion')].find((p) => existsSync(p)),
);
const OUT = join(ROOT, 'src', 'content', 'ayuda');
mkdirSync(OUT, { recursive: true });
const mapa = JSON.parse(readFileSync(join(ROOT, 'src', 'data', 'tutoriales-mapa.json'), 'utf8'));
const porNumero = new Map(mapa.tutoriales.map((x) => [x.n, x.slug]));

const DOCS = [
  { src: '00-inicio/README.md', slug: 'que-es-adestock', orden: 1, title: 'Qué es ADEstock y dónde se hace cada cosa', syn: ['empezar', 'qué es adestock', 'glosario', 'roles', 'permisos', 'pos', 'panel', 'app del dueño'] },
  { src: '03-conceptos/README.md', slug: 'conceptos-clave', orden: 2, title: 'Conceptos clave: stock, precios, cuentas corrientes y turnos de caja', syn: ['conceptos', 'de dónde sale el stock', 'costo', 'rentabilidad', 'fiado', 'arqueo', 'turno'] },
  { src: '05-faq/README.md', slug: 'preguntas-frecuentes', orden: 3, title: 'Preguntas frecuentes y problemas comunes de ADEstock', syn: ['faq', 'problemas', 'errores', 'qué hago si', 'no me deja', 'no funciona'] },
];
const RUTAS = { '00-inicio': 'que-es-adestock', '03-conceptos': 'conceptos-clave', '05-faq': 'preguntas-frecuentes' };

const yaml = (v) => JSON.stringify(v);
const plain = (md) => md.replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').replace(/[*_`>#|]/g, '').replace(/\s+/g, ' ').trim();
const recortar = (s, max = 170) => (s.length <= max ? s : s.slice(0, max - 1).replace(/\s\S*$/, '').replace(/[.,;:]$/, '') + '…');

for (const d of DOCS) {
  const raw = readFileSync(join(DOC, d.src), 'utf8');
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  const meta = {};
  for (const l of m[1].split(/\r?\n/)) {
    const i = l.indexOf(':');
    if (i > 0) meta[l.slice(0, i).trim()] = l.slice(i + 1).trim();
  }
  let body = raw.slice(m[0].length).replace(/^\s*# .*\r?\n/, '');

  // Enlaces a tutoriales y a otras páginas de ayuda
  body = body.replace(/\]\(\.\.\/01-manual-usuario\/(\d\d)-[a-z0-9-]+\.md(#[^)]*)?\)/g, (x, n, a) =>
    porNumero.has(n) ? `](/tutoriales/${porNumero.get(n)}/${a ?? ''})` : x,
  );
  // Enlaces sin la carpeta (NN-nombre.md) y al índice general de la documentación
  body = body.replace(/\]\((\d\d)-[a-z0-9-]+\.md(#[^)]*)?\)/g, (x, n, a) =>
    porNumero.has(n) ? `](/tutoriales/${porNumero.get(n)}/${a ?? ''})` : x,
  );
  body = body.replace(/\]\(\.\.\/README\.md(#[^)]*)?\)/g, '](/tutoriales/)');
  body = body.replace(/\]\(\.\.\/(00-inicio|03-conceptos|05-faq)\/README\.md(#[^)]*)?\)/g, (x, dir, a) => `](/ayuda/${RUTAS[dir]}/${a ?? ''})`);
  body = body.replace(/\]\((00-inicio|03-conceptos|05-faq)\/README\.md(#[^)]*)?\)/g, (x, dir, a) => `](/ayuda/${RUTAS[dir]}/${a ?? ''})`);

  const primero = body.split(/\n{2,}/).map((b) => b.trim()).find((b) => b && !b.startsWith('#') && !b.startsWith('>') && !b.startsWith('|'));
  const out = join(OUT, `${d.slug}.md`);
  const previo = {};
  if (existsSync(out)) {
    for (const l of readFileSync(out, 'utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/)[1].split(/\r?\n/)) {
      const i = l.indexOf(':');
      if (i > 0) { try { previo[l.slice(0, i)] = JSON.parse(l.slice(i + 1)); } catch { /* ignorar */ } }
    }
  }
  const fm = {
    id: d.slug,
    slug: d.slug,
    title: previo.title ?? d.title,
    description: previo.description ?? recortar(plain(primero ?? d.title)),
    orden: d.orden,
    status: previo.status ?? 'draft',
    source_path: d.src,
    source_hash: createHash('sha256').update(raw).digest('hex'),
    product_version:
      previo.product_version && previo.product_version !== 'pendiente-verificar'
        ? previo.product_version
        : (String(meta.version_sistema ?? '').match(/\d+\.\d+\.\d+/) ?? ['pendiente-verificar'])[0],
    verified_at: (meta.verificado.match(/\d{4}-\d{2}-\d{2}/) ?? [''])[0],
    reviewed_at: previo.reviewed_at ?? null,
    reviewed_by: previo.reviewed_by ?? null,
    synonyms: d.syn,
    social_image: previo.social_image ?? null,
  };
  writeFileSync(out, `---\n${Object.entries(fm).map(([k, v]) => `${k}: ${yaml(v)}`).join('\n')}\n---\n${body.trimStart()}`);
  console.log(`${d.slug.padEnd(24)} ${body.split(/\s+/).length} palabras`);
}
