// Migra las páginas heredadas con estilos en línea (casos de uso, gestión, legales) al layout común.
// Conserva el TEXTO y los enlaces; descarta estilos, íconos y estructura visual vieja, que se reemplazan por el
// sistema de la home. Uso: node scripts/migrar_inline.mjs
// Salida: src/paginas/<slug>.html (contenido) y src/pages/<slug>.html.astro (cabecera + layout).
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from 'node-html-parser';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const PUBLIC = join(ROOT, 'public');
const PAGINAS = [
  'casos-uso-almacen-dietetica', 'casos-uso-minimarket', 'casos-uso-distribuidora-belleza',
  'gestion-inventario-avanzada', 'gestion-multi-deposito', 'multiples-cajas-pos',
  'politica-privacidad', 'terminos-condiciones',
];
const KEEP = new Set(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'strong', 'b', 'em', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'details', 'summary', 'blockquote']);
const DROP = new Set(['script', 'style', 'svg', 'i', 'nav', 'header', 'footer', 'form', 'button', 'noscript', 'link', 'meta', 'input', 'select', 'textarea', 'dialog']);

const ent = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const esc = (s) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;');

function href(v) {
  if (!v || v === '#') return null;
  if (/^(https?:|mailto:|tel:)/.test(v)) return v;
  let h = v.replace(/^(\.\/|\.\.\/)+/, '');
  if (h.startsWith('#')) return h;
  if (/^index\.html/.test(h)) return '/' + h.replace(/^index\.html/, '');
  return h.startsWith('/') ? h : '/' + h;
}

function limpiar(node, out) {
  if (node.nodeType === 3) { // texto
    const t = node.rawText;
    if (t.trim()) out.push(t.replace(/\s+/g, ' '));
    return;
  }
  const tag = node.tagName?.toLowerCase();
  if (!tag) { node.childNodes.forEach((c) => limpiar(c, out)); return; }
  if (DROP.has(tag)) return;
  if (tag === 'a') {
    const h = href(node.getAttribute('href'));
    const interior = []; node.childNodes.forEach((c) => limpiar(c, interior));
    const texto = interior.join('').trim();
    if (!texto) return;
    if (h) out.push(`<a href="${esc(h)}">${texto}</a>`);
    else if (/descargar/i.test(texto)) out.push(`<a href="/descargar-demo.html">${texto}</a>`);
    else out.push(texto);
    return;
  }
  if (tag === 'iframe') {
    const src = node.getAttribute('src') ?? '';
    if (/youtube/.test(src)) {
      const id = (src.match(/embed\/([\w-]+)/) ?? [])[1];
      if (id) out.push(`<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/${id}" title="${esc(node.getAttribute('title') ?? 'Video de ADEstock')}" loading="lazy" allowfullscreen></iframe></div>`);
    }
    return;
  }
  if (tag === 'img') return; // imágenes de la maqueta anterior
  const interior = []; node.childNodes.forEach((c) => limpiar(c, interior));
  const html = interior.join('');
  if (KEEP.has(tag)) {
    if (!html.trim() && tag !== 'br') return;
    out.push(tag === 'br' ? '<br>' : `<${tag}>${html}</${tag}>`);
  } else {
    out.push(html); // div, section, article, span...: se desenvuelve
  }
}

for (const slug of PAGINAS) {
  const origen = join(PUBLIC, `${slug}.html`);
  if (!existsSync(origen)) { console.log(`(ya migrada) ${slug}`); continue; }
  const src = readFileSync(origen, 'utf8');
  const title = ent((src.match(/<title>([\s\S]*?)<\/title>/) ?? [])[1] ?? '').trim();
  const description = ent((src.match(/name="description" content="([^"]*)"/) ?? [])[1] ?? '');
  const jsonLd = [...src.matchAll(/<script[^>]+application\/ld\+json[^>]*>([\s\S]*?)<\/script>/g)].map((m) => JSON.parse(m[1]));

  const doc = parse(src);
  const raiz = doc.querySelector('main') ?? doc.querySelector('body');
  const out = [];
  raiz.childNodes.forEach((c) => limpiar(c, out));
  let html = out.join('\n')
    .replace(/<p>\s*\d{1,2}\s*<\/p>/g, '') // números sueltos de pasos
    .replace(/<(p|li|h[1-4]|summary|td|th)>\s*<\/\1>/g, '')
    .replace(/\s*—\s*/g, ' - ')
    .replace(/\n{2,}/g, '\n');

  // Hero: primer h1 (o primer h2) + primer párrafo siguiente
  let h1 = (html.match(/<h1>([\s\S]*?)<\/h1>/) ?? [])[1];
  if (h1) html = html.replace(/<h1>[\s\S]*?<\/h1>\s*/, '');
  else { h1 = (html.match(/<h2>([\s\S]*?)<\/h2>/) ?? [])[1]; html = html.replace(/<h2>[\s\S]*?<\/h2>\s*/, ''); }
  const lead = (html.match(/^\s*<p>([\s\S]*?)<\/p>/) ?? [])[1] ?? '';
  if (lead) html = html.replace(/^\s*<p>[\s\S]*?<\/p>\s*/, '');
  const legal = /politica|terminos/.test(slug);

  const cuerpo = `<div class="crumbs"><a href="/">Inicio</a> / ${h1.replace(/<[^>]+>/g, '')}</div>
<main id="contenido">
<header class="page-hero"><div class="page-hero__inner"><h1>${h1}</h1>${lead ? `<p class="page-lead">${lead}</p>` : ''}</div></header>
<div class="prose${legal ? ' legal' : ''}">
${html}
</div>
<section class="band alt"><div class="seo-hero__inner"><h2 style="max-width:22ch">Probá ADEstock con tu negocio</h2><p class="page-lead">Descargá la demo y usala 3 días, o escribinos y lo vemos juntos.</p><div class="actions"><a class="btn btn-primary" href="/descargar-demo.html">Descargar la demo</a><a class="btn btn-ghost" href="/contacto.html">Contacto</a></div></div></section>
</main>
`.replace(legal ? /<section class="band alt">[\s\S]*?<\/section>\n/ : /$^/, '');
  mkdirSync(join(ROOT, 'src', 'paginas'), { recursive: true });
  writeFileSync(join(ROOT, 'src', 'paginas', `${slug}.html`), cuerpo);

  writeFileSync(join(ROOT, 'src', 'pages', `${slug}.html.astro`), `---
// Migrada desde public/${slug}.html. Contenido en src/paginas/${slug}.html.
import Pagina from '../layouts/Pagina.astro';
import contenido from '../paginas/${slug}.html?raw';
const jsonLd = ${JSON.stringify(jsonLd, null, 2)};
---
<Pagina
  title={${JSON.stringify(title)}}
  description={${JSON.stringify(description)}}
  path="/${slug}.html"
  jsonLd={jsonLd}
>
  <Fragment set:html={contenido} />
</Pagina>
`);
  const arch = join(ROOT, 'docs', 'legacy', 'paginas', `${slug}.html`);
  mkdirSync(dirname(arch), { recursive: true });
  renameSync(origen, arch);
  console.log(`OK ${slug}: ${html.length} bytes, ${jsonLd.length} JSON-LD`);
}
