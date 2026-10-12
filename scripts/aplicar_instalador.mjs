// Publica una nueva versión del instalador de escritorio en el sitio.
// Uso:  node scripts/aplicar_instalador.mjs <URL_DEL_.exe> [version]
//   ej: node scripts/aplicar_instalador.mjs https://github.com/adema-websites/adestock/releases/download/ADEstock-desktop-3.0.1v/Adestock_Installer_v3.0.1.exe 3.0.1
// Qué hace:
//  - Verifica que la URL responda 200 y sea un archivo (sin --forzar, aborta si no).
//  - Reemplaza el enlace vigente (el de la versión que figura en src/data/descargas.json) en las páginas públicas.
//  - Actualiza versiones.html con la plantilla docs/plantillas/versiones-instalador.html
//    (la release anterior queda debajo como "RELEASE ANTERIOR" con su propio enlace).
//  - Guarda la nueva versión en src/data/descargas.json.
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

const cfgPath = join(ROOT, 'src', 'data', 'descargas.json');
const cfg = JSON.parse(readFileSync(cfgPath, 'utf8'));
const previa = cfg.instalador;

// 1) La URL tiene que existir
try {
  const r = await fetch(url, { method: 'HEAD', redirect: 'follow' });
  console.log(`HEAD ${r.status} ${r.headers.get('content-length') ?? '?'} bytes`);
  if (!r.ok && !forzar) { console.error('La URL no responde 200. Usá --forzar si es a propósito.'); process.exit(1); }
} catch (e) {
  if (!forzar) { console.error('No pude consultar la URL:', e.message); process.exit(1); }
}

// 2) Enlaces del instalador vigente en páginas públicas
const paginas = ['descargar-demo.html', 'casos-uso-almacen-dietetica.html', 'casos-uso-minimarket.html', 'versiones.html'];
const conteo = {};
for (const p of paginas) {
  const f = join(ROOT, 'public', p);
  let s = readFileSync(f, 'utf8');
  const antes = s;
  // Importante: en versiones.html el historial conserva las releases anteriores; solo se reemplaza lo vigente.
  if (p !== 'versiones.html') {
    s = s.split(previa.url).join(url).split(previa.archivo).join(archivo);
  }
  if (s !== antes) { writeFileSync(f, s); conteo[p] = true; }
}

// 3) versiones.html: nueva release arriba, la anterior pasa a "RELEASE ANTERIOR"
{
  const f = join(ROOT, 'public', 'versiones.html');
  let s = readFileSync(f, 'utf8');
  if (s.includes(`ADEstock v${version}:`)) {
    console.log('versiones.html ya tiene esta versión; no se vuelve a insertar.');
  } else {
    const plantilla = readFileSync(join(ROOT, 'docs', 'plantillas', 'versiones-instalador.html'), 'utf8')
      .split('{{URL}}').join(url).split('{{ARCHIVO}}').join(archivo).split('{{VERSION}}').join(version);
    const ini = s.indexOf('<section', s.indexOf('NUEVA RELEASE') - 400);
    const iniReal = s.lastIndexOf('<section', s.indexOf('NUEVA RELEASE'));
    const finMarcador = s.indexOf('RELEASE ANTERIOR');
    const finReal = s.lastIndexOf('<section', finMarcador);
    if (iniReal < 0 || finReal < 0 || finReal < iniReal) { console.error('No encontré los marcadores en versiones.html'); process.exit(1); }
    // La release vigente hasta hoy se conserva, pero como "anterior" y sin el bloque de "Instalación / actualización" técnico.
    const vieja = s.slice(iniReal, finReal)
      .replace('NUEVA RELEASE', 'RELEASE ANTERIOR')
      .replace('background: #1d4ed8', 'background: #0f766e')
      .replace('Última versión estable publicada:', 'Versión estable anterior:');
    s = s.slice(0, iniReal) + plantilla + vieja + s.slice(finReal);
    writeFileSync(f, s);
    conteo['versiones.html'] = true;
  }
}

// 4) Registro
cfg.instalador = { version, url, archivo, publicado: new Date().toISOString().slice(0, 10) };
cfg.historial = [{ ...previa }, ...(cfg.historial ?? [])];
writeFileSync(cfgPath, JSON.stringify(cfg, null, 2) + '\n');
console.log('Actualizado:', Object.keys(conteo).join(', ') || '(nada)');
console.log(`Instalador vigente: v${version} -> ${url}`);
