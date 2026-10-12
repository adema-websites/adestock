// Publica una nueva versión del instalador de escritorio en el sitio.
// Uso:  node scripts/aplicar_instalador.mjs <URL_DEL_.exe> [version] [--forzar]
//   ej: node scripts/aplicar_instalador.mjs https://github.com/adema-websites/adestock/releases/download/ADEstock-desktop-3.0.1v/Adestock_Installer_v3.0.1.exe 3.0.1
// Qué hace: verifica que la URL responda, y actualiza src/data/descargas.json (versión vigente) y
// src/data/versiones.json (hace visible la versión y le asigna el enlace). Las páginas de descarga, novedades,
// casos de uso y llms.txt leen esos datos, así que se actualizan solas en el próximo build.
import { readFileSync, writeFileSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const [url, versionArg] = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const forzar = process.argv.includes('--forzar');
if (!url) { console.error('Falta la URL del instalador.'); process.exit(1); }

const archivo = basename(new URL(url).pathname);
const version = versionArg ?? (archivo.match(/(\d+\.\d+\.\d+)/) ?? [])[1];
if (!version) { console.error('No pude deducir la versión; pasala como segundo argumento.'); process.exit(1); }

try {
  const r = await fetch(url, { method: 'HEAD', redirect: 'follow' });
  console.log(`HEAD ${r.status} ${r.headers.get('content-length') ?? '?'} bytes`);
  if (!r.ok && !forzar) { console.error('La URL no responde 200. Usá --forzar si es a propósito.'); process.exit(1); }
} catch (e) {
  if (!forzar) { console.error('No pude consultar la URL:', e.message); process.exit(1); }
}

const leer = (f) => JSON.parse(readFileSync(join(ROOT, 'src', 'data', f), 'utf8'));
const guardar = (f, d) => writeFileSync(join(ROOT, 'src', 'data', f), JSON.stringify(d, null, 2) + '\n');

// descargas.json
const cfg = leer('descargas.json');
if (cfg.instalador.version !== version) cfg.historial = [{ ...cfg.instalador }, ...(cfg.historial ?? [])];
cfg.instalador = { version, url, archivo, publicado: new Date().toISOString().slice(0, 10) };
guardar('descargas.json', cfg);

// versiones.json
const v = leer('versiones.json');
const entrada = v.versiones.find((x) => x.version === version);
if (!entrada) {
  console.warn(`Aviso: versiones.json no tiene una entrada para ${version}. Agregala (novedades) para que figure en /versiones.html.`);
} else {
  entrada.visible = true;
  entrada.url = url;
  entrada.archivo = archivo;
}
guardar('versiones.json', v);
console.log(`Instalador vigente: v${version} -> ${url}`);
console.log(entrada ? 'Novedades visibles en /versiones.html.' : 'Falta cargar sus novedades en versiones.json.');
