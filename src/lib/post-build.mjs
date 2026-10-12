// Integración de Astro que corre al terminar el build:
//  1. Las páginas con URL ".html" (precios.html, contacto.html...) Astro las genera como carpeta/index.html.
//     Se mueven a archivo para conservar exactamente la URL anterior (sin redirección).
//  2. Genera sitemap.xml escaneando dist/: solo páginas con canonical propio, sin noindex.
//     lastmod: el heredado del sitemap anterior, o dateModified del JSON-LD (guías revisadas). Sin fecha real no se escribe.
import { existsSync, readdirSync, readFileSync, renameSync, rmdirSync, statSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const SITE = 'https://adestock.com.ar';

function recorrer(dir, fn) {
  for (const n of readdirSync(dir)) {
    const p = join(dir, n);
    if (statSync(p).isDirectory()) recorrer(p, fn);
    else fn(p);
  }
}

export default function postBuild({ heredado }) {
  return {
    name: 'adestock-post-build',
    hooks: {
      'astro:build:done': ({ dir, logger }) => {
        const dist = fileURLToPath(dir);

        // 1) carpeta.html/index.html -> carpeta.html
        const movidas = [];
        (function buscar(d) {
          for (const n of readdirSync(d)) {
            const p = join(d, n);
            if (!statSync(p).isDirectory()) continue;
            if (n.endsWith('.html') && existsSync(join(p, 'index.html'))) {
              const tmp = p + '.__tmp';
              renameSync(join(p, 'index.html'), tmp);
              try { rmdirSync(p); } catch { /* no vacía */ }
              renameSync(tmp, p);
              movidas.push(relative(dist, p));
            } else buscar(p);
          }
        })(dist);
        if (movidas.length) logger.info(`.html como archivo: ${movidas.join(', ')}`);

        // 2) sitemap
        const urls = new Map();
        recorrer(dist, (f) => {
          if (!f.endsWith('.html')) return;
          const rel = relative(dist, f).replace(/\\/g, '/');
          if (rel === '404.html') return;
          const html = readFileSync(f, 'utf8');
          if (/<meta[^>]+name=["']robots["'][^>]*noindex/i.test(html)) return;
          const canon = html.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i)?.[1];
          if (!canon || !canon.startsWith(SITE + '/')) return;
          const mod = html.match(/"dateModified":"(\d{4}-\d{2}-\d{2})/)?.[1] ?? heredado.get(canon);
          urls.set(canon, mod);
        });
        const cuerpo = [...urls]
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([loc, m]) => `  <url><loc>${loc}</loc>${m ? `<lastmod>${m}</lastmod>` : ''}</url>`)
          .join('\n');
        writeFileSync(join(dist, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${cuerpo}\n</urlset>\n`);
        logger.info(`sitemap.xml: ${urls.size} URLs`);
      },
    },
  };
}
