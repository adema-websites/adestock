// Captura de páginas para revisión visual. Uso: node scripts/web-capturas/paginas.mjs <carpeta_salida> <ruta> [ruta...]
// Cada ruta se guarda en escritorio (1440) y celular (390), a página completa. Base: http://localhost:4321
import { createRequire } from 'node:module';
import { join } from 'node:path';
const require = createRequire(import.meta.url);
const { chromium } = require(join(process.env.APPDATA, 'npm/node_modules/@playwright/cli/node_modules/playwright-core'));
const [out, ...rutas] = process.argv.slice(2);
const BASE = process.env.BASE ?? 'http://localhost:4321';
const b = await chromium.launch();
for (const [etq, ancho, alto] of [['d', 1440, 900], ['m', 390, 844]]) {
  const p = await (await b.newContext({ viewport: { width: ancho, height: alto } })).newPage();
  const errores = [];
  p.on('pageerror', (e) => errores.push(e.message));
  p.on('requestfailed', (r) => errores.push('req ' + r.url().slice(0, 80)));
  for (const r of rutas) {
    await p.goto(BASE + (r.startsWith('/') ? r : '/' + r), { waitUntil: 'networkidle' });
    await p.evaluate(() => { document.querySelectorAll('.rev').forEach((e) => e.classList.add('in')); document.querySelectorAll('img[loading=lazy]').forEach((i) => (i.loading = 'eager')); });
    await p.waitForTimeout(700);
    const desborde = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    const nombre = r.replace(/[^a-z0-9]+/gi, '_').replace(/^_|_$/g, '') || 'home';
    await p.screenshot({ path: join(out, `${etq}_${nombre}.png`), fullPage: true });
    console.log(`${etq} ${r}${desborde > 1 ? '  DESBORDE ' + desborde + 'px' : ''}`);
  }
  if (errores.length) console.log(`  errores (${etq}):`, [...new Set(errores)].slice(0, 5).join(' | '));
}
await b.close();
