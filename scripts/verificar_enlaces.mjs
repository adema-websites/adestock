// Verifica los enlaces internos (y sus anclas) de dist/. Uso: npm run build && node scripts/verificar_enlaces.mjs
// Sale con código 1 si encuentra enlaces rotos. Ignora enlaces externos, mailto, tel y archivos de recursos ya servidos.
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const DIST = join(resolve(dirname(fileURLToPath(import.meta.url)), '..'), 'dist');
const htmls = [];
(function recorrer(d) {
  for (const n of readdirSync(d)) {
    const p = join(d, n);
    if (statSync(p).isDirectory()) recorrer(p);
    else if (n.endsWith('.html')) htmls.push(p);
  }
})(DIST);

const aRuta = (url) => {
  let r = url.replace(/^\//, '');
  if (r === '' || r.endsWith('/')) r += 'index.html';
  return join(DIST, r);
};
const cacheIds = new Map();
const idsDe = (archivo) => {
  if (!cacheIds.has(archivo)) {
    const s = readFileSync(archivo, 'utf8');
    cacheIds.set(archivo, new Set([...s.matchAll(/\sid=["']([^"']+)["']/g)].map((m) => m[1])));
  }
  return cacheIds.get(archivo);
};

const rotos = [];
let total = 0;
for (const f of htmls) {
  const rel = f.replace(DIST, '').replace(/\\/g, '/');
  const html = readFileSync(f, 'utf8');
  // Se ignoran páginas legadas con navegación heredada: se revisan igual, pero solo se informan enlaces absolutos del sitio.
  for (const m of html.matchAll(/<a\s[^>]*href=["']([^"'#?][^"']*|#[^"']*)["']/g)) {
    const href = m[1];
    if (/^(https?:|mailto:|tel:|javascript:|data:)/i.test(href)) continue;
    let [ruta, ancla] = href.split('#');
    ruta = ruta.split('?')[0];
    let destino;
    if (ruta === '') destino = f;
    else if (ruta.startsWith('/')) destino = aRuta(ruta);
    else destino = resolve(dirname(f), ruta.endsWith('/') ? ruta + 'index.html' : ruta);
    total++;
    let ok = existsSync(destino) && statSync(destino).isFile();
    if (!ok && existsSync(destino + '/index.html')) { destino = destino + '/index.html'; ok = true; }
    if (!ok) { rotos.push(`${rel} -> ${href} (no existe)`); continue; }
    if (ancla && destino.endsWith('.html') && !idsDe(destino).has(decodeURIComponent(ancla))) rotos.push(`${rel} -> ${href} (ancla inexistente)`);
  }
}
console.log(`Enlaces internos revisados: ${total} en ${htmls.length} páginas`);
if (rotos.length) {
  const unicos = [...new Set(rotos)];
  console.log(`\nROTOS (${unicos.length}):\n` + unicos.slice(0, 80).join('\n'));
  process.exitCode = 1;
} else console.log('Sin enlaces rotos.');
