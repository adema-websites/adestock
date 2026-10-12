// Migra las páginas SEO estáticas (public/<ruta>/index.html, estructura seo-*) a páginas Astro con el
// layout común (nav, pie, tipografía y fondos de la home).
// Uso: node scripts/migrar_seo.mjs            (migra la lista de abajo; mueve el original a docs/legacy/paginas/)
// El contenido (migas, hero, main) queda en src/paginas/<slug>.html; los datos de cabecera, en el .astro generado.
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join, posix, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const PUBLIC = join(ROOT, 'public');
const RUTAS = [
  'sistema-de-stock', 'control-de-stock', 'control-de-inventarios', 'software-de-inventario-argentina',
  'sistema-de-stock-para-kioscos', 'sistema-de-stock-para-almacenes', 'sistema-de-stock-para-minimarkets',
  'blog', 'blog/como-controlar-inventario-almacen', 'blog/como-controlar-stock-kiosco',
  'blog/como-evitar-faltantes-de-mercaderia', 'blog/que-debe-tener-un-sistema-de-stock-para-comercios',
  'blog/sistema-de-stock-vs-excel', 'blog/stock-minimo-compras-reposicion',
];

const ent = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const meta = (html, re) => (html.match(re) ?? [])[1] ?? '';

for (const ruta of RUTAS) {
  const origen = join(PUBLIC, ruta, 'index.html');
  if (!existsSync(origen)) { console.log(`(salteada, ya migrada) ${ruta}`); continue; }
  const html = readFileSync(origen, 'utf8');
  const url = `/${ruta}/`;

  const title = ent(meta(html, /<title>([\s\S]*?)<\/title>/));
  const description = ent(meta(html, /<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/));
  const ogType = meta(html, /<meta[^>]+property=["']og:type["'][^>]+content=["']([^"']*)["']/) || 'website';
  const jsonLd = [...html.matchAll(/<script[^>]+application\/ld\+json[^>]*>([\s\S]*?)<\/script>/g)].map((m) => JSON.parse(m[1]));

  const migas = meta(html, /(<div class="seo-breadcrumbs">[\s\S]*?<\/div>)/);
  const hero = meta(html, /(<header class="seo-hero">[\s\S]*?<\/header>)/);
  let main = meta(html, /<main[^>]*>([\s\S]*?)<\/main>/);
  if (!hero || !main) { console.error(`NO MIGRADA ${ruta}: sin hero o main`); continue; }

  // Enlaces y recursos relativos -> absolutos del sitio
  const absoluto = (v) => {
    if (/^(https?:|mailto:|tel:|#|\/)/.test(v)) return v;
    const [p, h] = v.split('#');
    const r = posix.normalize(posix.join(url, p));
    return r + (h ? '#' + h : '');
  };
  const reescribir = (s) => s.replace(/(href|src)="([^"]+)"/g, (_, a, v) => `${a}="${absoluto(v)}"`);

  const cuerpo = `${reescribir(migas)}\n${reescribir(hero)}\n<main id="contenido">${reescribir(main)}</main>\n`;
  const slug = ruta.replace(/\//g, '--');
  mkdirSync(join(ROOT, 'src', 'paginas'), { recursive: true });
  writeFileSync(join(ROOT, 'src', 'paginas', `${slug}.html`), cuerpo);

  const profundidad = ruta.split('/').length + 1; // src/pages/<ruta>/index.astro
  const rel = '../'.repeat(profundidad);
  const astro = `---
// Migrada desde public/${ruta}/index.html. El contenido vive en src/paginas/${slug}.html.
import Pagina from '${rel}layouts/Pagina.astro';
import contenido from '${rel}paginas/${slug}.html?raw';
const jsonLd = ${JSON.stringify(jsonLd, null, 2)};
---
<Pagina
  title={${JSON.stringify(title)}}
  description={${JSON.stringify(description)}}
  path="${url}"
  ogType="${ogType === 'article' ? 'article' : 'website'}"
  jsonLd={jsonLd}
>
  <Fragment set:html={contenido} />
</Pagina>
`;
  const destino = join(ROOT, 'src', 'pages', ruta, 'index.astro');
  mkdirSync(dirname(destino), { recursive: true });
  writeFileSync(destino, astro);

  const arch = join(ROOT, 'docs', 'legacy', 'paginas', slug + '.html');
  mkdirSync(dirname(arch), { recursive: true });
  renameSync(origen, arch);
  console.log(`OK ${ruta}  (${jsonLd.length} JSON-LD, ${cuerpo.length} bytes)`);
}
