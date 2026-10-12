import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { SITE, categorias, esBorrador, getAyuda, getTutoriales } from '../lib/tutoriales';

// Sitemap generado en el build: solo URLs canónicas, públicas e indexables.
//  - Páginas estáticas de public/: se leen sus <link rel=canonical> y se excluyen las que declaran noindex.
//  - Centro de ayuda: solo si hay al menos un tutorial publicado (los borradores nunca entran).
//  - lastmod: el heredado del sitemap anterior para las páginas que ya existían, y reviewed_at para los tutoriales.
//    Sin fecha real no se escribe lastmod (no se inventa).
const PUBLIC = join(process.cwd(), 'public');

function htmls(dir: string): string[] {
  return readdirSync(dir).flatMap((n) => {
    const p = join(dir, n);
    return statSync(p).isDirectory() ? htmls(p) : n.endsWith('.html') ? [p] : [];
  });
}

const heredado = new Map<string, string>();
const xmlViejo = readFileSync(join(process.cwd(), 'src/data/sitemap-lastmod-heredado.xml'), 'utf8');
for (const m of xmlViejo.matchAll(/<loc>([^<]+)<\/loc>\s*<lastmod>([^<]+)<\/lastmod>/g)) heredado.set(m[1].trim(), m[2].trim());

export async function GET() {
  const urls = new Map<string, string | undefined>();

  for (const f of htmls(PUBLIC)) {
    const html = readFileSync(f, 'utf8');
    const rel = relative(PUBLIC, f).replace(/\\/g, '/');
    if (rel === '404.html') continue;
    if (/<meta[^>]+name=["']robots["'][^>]*noindex/i.test(html)) continue;
    const canon = html.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i)?.[1];
    if (!canon) { console.warn(`[sitemap] ${rel}: sin canonical, se omite`); continue; }
    if (!canon.startsWith(SITE + '/')) { console.warn(`[sitemap] ${rel}: canonical externo, se omite`); continue; }
    urls.set(canon, urls.get(canon) ?? heredado.get(canon));
  }

  const publicados = (await getTutoriales()).filter((t) => !esBorrador(t));
  if (publicados.length > 0) {
    urls.set(`${SITE}/tutoriales/`, undefined);
    urls.set(`${SITE}/tutoriales/empezar/`, undefined);
    for (const cat of Object.keys(categorias)) {
      if (publicados.some((t) => t.data.category === cat)) urls.set(`${SITE}/tutoriales/categorias/${cat}/`, undefined);
    }
    for (const t of publicados) urls.set(`${SITE}/tutoriales/${t.data.slug}/`, t.data.reviewed_at ?? undefined);
  }

  for (const a of (await getAyuda()).filter((x) => !esBorrador(x))) {
    urls.set(`${SITE}/ayuda/${a.data.slug}/`, a.data.reviewed_at ?? undefined);
  }

  const cuerpo = [...urls]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([loc, mod]) => `  <url><loc>${loc}</loc>${mod ? `<lastmod>${mod}</lastmod>` : ''}</url>`)
    .join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${cuerpo}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
