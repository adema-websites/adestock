// Genera las tarjetas sociales 1200x630 (JPG) en public/social/ y las enlaza en el frontmatter de los tutoriales P0.
// Herramienta de desarrollo (no corre en el build): usa Chrome vía `playwright-cli` para tener tipografía confiable.
// Uso:  node scripts/generar_tarjetas.mjs [--todas]     (por defecto solo P0 + tarjeta general)
// Al cambiar el diseño o el texto de una tarjeta, subir VERSION: las redes cachean por URL (plan, sección 15).
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { createServer } from 'node:http';
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const VERSION = 'v1';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = join(ROOT, 'public', 'social');
const TMP = join(process.env.TEMP ?? ROOT, 'adestock-tarjetas');
const TUT = join(ROOT, 'src', 'content', 'tutoriales');
const PORT = 4577;
const elegidas = JSON.parse(readFileSync(join(ROOT, 'src', 'data', 'tarjetas-imagenes.json'), 'utf8'));
mkdirSync(OUT, { recursive: true });
mkdirSync(TMP, { recursive: true });

const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

const html = ({ etiqueta, titulo, bajada, img }) => `<!doctype html><html lang="es"><meta charset="utf-8"><style>
*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;font-family:"Segoe UI",Arial,sans-serif;background:linear-gradient(135deg,#0f2a6b,#2563eb);color:#fff;display:flex;overflow:hidden}
.t{flex:1;padding:56px 24px 48px 64px;display:flex;flex-direction:column;justify-content:space-between}
.marca{font-size:34px;font-weight:800;letter-spacing:.5px}.marca span{color:#67e8f9}
.et{display:inline-block;margin-top:34px;background:#fff;color:#1d4ed8;font-weight:700;font-size:22px;padding:6px 16px;border-radius:999px}
h1{margin:20px 0 0;font-size:${titulo.length > 62 ? 46 : 54}px;line-height:1.12;font-weight:800}
p{margin:18px 0 0;font-size:26px;opacity:.9}.url{font-size:24px;opacity:.85}
.i{width:470px;display:flex;align-items:center;padding-right:48px}
.i div{width:100%;height:380px;border-radius:16px;background:#fff url("${img ?? ''}") left top/cover no-repeat;box-shadow:0 20px 50px rgba(0,0,0,.35);border:6px solid #fff;${img ? '' : 'display:none'}}
</style><body><div class="t"><div><div class="marca">AD<span>E</span>stock</div><span class="et">${esc(etiqueta)}</span><h1>${esc(titulo)}</h1>${bajada ? `<p>${esc(bajada)}</p>` : ''}</div><div class="url">adestock.com.ar</div></div>${img ? '<div class="i"><div></div></div>' : ''}</body></html>`;

// Tutoriales objetivo
const todas = process.argv.includes('--todas');
const tutoriales = readdirSync(TUT).filter((f) => f.endsWith('.md')).map((f) => {
  const raw = readFileSync(join(TUT, f), 'utf8');
  const fm = (k) => JSON.parse((raw.match(new RegExp(`^${k}: (.*)$`, 'm')) ?? [])[1] ?? 'null');
  const primera = raw.match(/\]\(\.\.\/\.\.\/assets\/tutoriales\/([^)]+)\)/);
  return { archivo: join(TUT, f), raw, slug: fm('slug'), titulo: fm('title'), prio: fm('priority'), img: elegidas[fm('slug')] ?? primera?.[1] };
}).filter((t) => todas || t.prio === 'P0');

const tarjetas = [
  { id: 'adestock', etiqueta: 'Sistema de stock y ventas', titulo: 'Vendé y controlá el stock de tu comercio', bajada: 'Productos, ventas, compras y caja en un solo sistema.' },
  { id: 'tutoriales', etiqueta: 'Centro de ayuda', titulo: 'Tutoriales de ADEstock paso a paso', bajada: 'Aprendé a vender, controlar el stock y cargar compras con foto.' },
  ...tutoriales.map((t) => ({ id: t.slug, etiqueta: 'Tutorial', titulo: t.titulo.replace(/ en ADEstock$/, ''), t })),
];

const server = createServer((req, res) => {
  const p = join(TMP, decodeURIComponent(req.url.split('?')[0]));
  if (!existsSync(p)) { res.writeHead(404).end(); return; }
  res.writeHead(200, { 'Content-Type': p.endsWith('.html') ? 'text/html; charset=utf-8' : 'image/png' }).end(readFileSync(p));
}).listen(PORT);

// Async: el servidor HTTP vive en este mismo proceso y no puede quedar bloqueado.
const run = promisify(execFile);
const cli = (...a) => run('playwright-cli', a, { shell: true });
await cli('open', `http://localhost:${PORT}/x.html`).catch(() => {}); // 404 esperado: solo abre el navegador
await cli('resize', '1200', '630');

for (const c of tarjetas) {
  let img = null;
  if (c.t?.img) {
    const src = join(ROOT, 'src', 'assets', 'tutoriales', c.t.img);
    if (existsSync(src)) { copyFileSync(src, join(TMP, `${c.id}.png`)); img = `${c.id}.png`; }
  }
  writeFileSync(join(TMP, `${c.id}.html`), html({ ...c, img }));
  await cli('goto', `http://localhost:${PORT}/${c.id}.html`);
  const png = join(TMP, `${c.id}-shot.png`);
  await cli('screenshot', `--filename="${png}"`);
  const destino = `${c.id}-${VERSION}.jpg`;
  await sharp(png).resize(1200, 630).jpeg({ quality: 86, mozjpeg: true }).toFile(join(OUT, destino));
  if (c.t) {
    const nuevo = c.t.raw.replace(/^social_image: .*$/m, `social_image: "/social/${destino}"`);
    if (nuevo !== c.t.raw) writeFileSync(c.t.archivo, nuevo);
  }
  console.log('  ' + destino);
}
await cli('close');
server.close();
console.log(`\n${tarjetas.length} tarjetas en public/social/`);
