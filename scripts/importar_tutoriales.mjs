// Importa los tutoriales del manual de usuario a src/content/tutoriales (borradores).
// Uso:  node scripts/importar_tutoriales.mjs [ruta/01-manual-usuario]
// - Conserva source_path y source_hash; nunca marca nada como revisado ni publicado.
// - Copia solo las carpetas de imágenes referenciadas a src/assets/tutoriales/<carpeta>/ (Astro genera WebP/srcset).
// - Si un tutorial ya existe, conserva su estado editorial (status, reviewed_at, product_version, related,
//   social_image, title, description) y solo actualiza el contenido y la huella del origen.
import { createHash } from 'node:crypto';
import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = resolve(process.argv[2] ?? join(ROOT, '..', 'documentacion', '01-manual-usuario'));
const OUT = join(ROOT, 'src', 'content', 'tutoriales');
const ASSETS = join(ROOT, 'src', 'assets', 'tutoriales');
const mapa = JSON.parse(readFileSync(join(ROOT, 'src', 'data', 'tutoriales-mapa.json'), 'utf8'));
mkdirSync(OUT, { recursive: true });

const files = readdirSync(SRC).filter((f) => /^\d\d-.*\.md$/.test(f));
const yaml = (v) => JSON.stringify(v); // JSON es YAML válido y escapa bien tildes y comillas

function parseFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!m) throw new Error('sin frontmatter');
  const meta = {};
  for (const line of m[1].split(/\r?\n/)) {
    const i = line.indexOf(':');
    if (i > 0) meta[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return { meta, body: text.slice(m[0].length) };
}

function plain(md) {
  return md
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/[*_`>#]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}
function recortar(s, max = 158) {
  if (s.length <= max) return s;
  const c = s.slice(0, max - 1);
  return c.slice(0, c.lastIndexOf(' ')).replace(/[.,;:]$/, '') + '…';
}

const resumen = [];
for (const t of mapa.tutoriales) {
  const file = files.find((f) => f.startsWith(t.n + '-'));
  if (!file) {
    console.error(`FALTA origen para ${t.n} (${t.slug})`);
    process.exitCode = 1;
    continue;
  }
  const raw = readFileSync(join(SRC, file), 'utf8');
  const { meta, body: b0 } = parseFrontmatter(raw);
  let body = b0.replace(/^\s*# .*\r?\n/, '');

  // "Para quién es / Tiempo / Necesitás" pasa a metadatos
  let tiempo = '', necesitas = '', para = '';
  body = body.replace(
    /^\s*> \*\*Para quién es:\*\*\s*(.*?)\s*\*\*Tiempo:\*\*\s*(.*?)\s*\*\*Necesitás:\*\*\s*(.*?)\s*\r?\n/m,
    (_, a, b, c) => {
      para = a.replace(/\.$/, '');
      tiempo = b.replace(/\.$/, '');
      necesitas = c.replace(/\.$/, '');
      return '';
    },
  );

  // Descripción = primer párrafo de "Qué vas a lograr"
  const lograr = body.match(/## Qué vas a lograr\s*\r?\n+([\s\S]*?)(\r?\n\r?\n|$)/);
  const description = recortar(plain(lograr ? lograr[1] : meta.titulo));

  // Imágenes referenciadas
  const imgs = new Set();
  body = body.replace(/\]\(imagenes\/([^/)]+)\/([^)]+)\)/g, (_, dir, f) => {
    imgs.add(dir);
    return `](../../assets/tutoriales/${dir}/${f})`;
  });
  for (const dir of imgs) {
    const from = join(SRC, 'imagenes', dir);
    if (existsSync(from)) cpSync(from, join(ASSETS, dir), { recursive: true });
    else console.error(`  carpeta de imágenes faltante: ${dir}`);
  }

  const outFile = join(OUT, `${t.slug}.md`);
  const previo = {};
  if (existsSync(outFile)) {
    const fmPrev = readFileSync(outFile, 'utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/)[1];
    for (const l of fmPrev.split(/\r?\n/)) {
      const i = l.indexOf(':');
      if (i > 0) { try { previo[l.slice(0, i)] = JSON.parse(l.slice(i + 1)); } catch { /* ignorar */ } }
    }
  }
  const fm = {
    id: t.slug,
    slug: t.slug,
    title: previo.title ?? t.titulo,
    description: previo.description ?? description,
    category: t.cat,
    priority: t.prio,
    roles: t.roles,
    surface: t.surface,
    status: previo.status ?? 'draft',
    tiempo,
    necesitas,
    para_quien: para,
    modulo: meta.modulo,
    permiso: meta.permiso,
    source_path: `01-manual-usuario/${file}`,
    source_hash: createHash('sha256').update(raw).digest('hex'),
    product_version: previo.product_version ?? meta.version_sistema ?? 'pendiente-verificar',
    verified_at: (meta.verificado.match(/\d{4}-\d{2}-\d{2}/) ?? [''])[0],
    reviewed_at: previo.reviewed_at ?? null,
    synonyms: t.syn,
    related: previo.related ?? [],
    social_image: previo.social_image ?? null,
  };
  const head = Object.entries(fm).map(([k, v]) => `${k}: ${yaml(v)}`).join('\n');
  writeFileSync(outFile, `---\n${head}\n---\n${body.trimStart()}`);
  resumen.push(`${t.n} ${t.slug.padEnd(40)} ${imgs.size} carpeta(s) de imágenes, ${body.split(/\s+/).length} palabras`);
}
console.log(resumen.join('\n'));
console.log(`\n${resumen.length}/${mapa.tutoriales.length} importados en src/content/tutoriales`);
