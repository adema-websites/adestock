// Base común para capturar imágenes y videos LIMPIOS (sin flechas) de la demo para la web comercial.
// Requiere la demo corriendo en DEMO_URL (por defecto http://127.0.0.1:8765, ver documentacion/_herramientas/demo).
// Salida: src/assets/web/ (imágenes, las optimiza Astro) y public/video/ (videos webm).
import { createRequire } from 'node:module';
import { mkdirSync, renameSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require(join(process.env.APPDATA, 'npm/node_modules/@playwright/cli/node_modules/playwright-core'));

export const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
export const IMG = join(ROOT, 'src', 'assets', 'web');
export const VID = join(ROOT, 'public', 'video');
export const BASE = process.env.DEMO_URL || 'http://127.0.0.1:8765';
mkdirSync(IMG, { recursive: true });
mkdirSync(VID, { recursive: true });

// opts: { ancho, alto, movil, video: 'nombre' }
export async function abrir({ ancho = 1440, alto = 900, movil = false, video = null } = {}) {
  const browser = await chromium.launch();
  const tmpVid = join(process.env.TEMP ?? ROOT, 'adestock-video');
  const ctx = await browser.newContext({
    ...(movil
      ? { viewport: { width: 390, height: 780 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }
      : { viewport: { width: ancho, height: alto }, deviceScaleFactor: 1 }),
    locale: 'es-AR',
    ...(video ? { recordVideo: { dir: tmpVid, size: movil ? { width: 390, height: 780 } : { width: ancho, height: alto } } } : {}),
  });
  const page = await ctx.newPage();
  page.on('dialog', (d) => d.accept().catch(() => {}));
  const api = {
    page,
    pausa: (ms) => page.waitForTimeout(ms),
    ir: async (ruta) => { await page.goto(BASE + ruta, { waitUntil: 'domcontentloaded' }); await page.waitForTimeout(700); },
    async login(usuario = 'dueno', clave = 'demo1234') {
      await api.ir('/login/');
      await page.fill('input[name="username"]', usuario);
      await page.fill('input[name="password"]', clave);
      await Promise.all([page.waitForLoadState('domcontentloaded'), page.click('button[type="submit"], input[type="submit"]')]);
      await page.waitForTimeout(800);
    },
    async abrirTurno(efectivo = '5000') {
      await api.ir('/pos/');
      const abrirT = page.locator('text=Abrir Turno');
      if (await abrirT.count() && await abrirT.first().isVisible()) {
        await page.fill('input[type="number"]:visible, input[inputmode="decimal"]:visible', efectivo).catch(() => {});
        await abrirT.first().click();
        await page.waitForTimeout(2000);
      }
    },
    async foto(nombre, opciones = {}) {
      const archivo = join(IMG, nombre + '.png');
      await page.screenshot({ path: archivo, ...opciones });
      console.log('  imagen →', archivo.replace(ROOT, '.'));
      return archivo;
    },
    async cerrar() {
      const v = video ? page.video() : null;
      await ctx.close();
      if (v) {
        const origen = await v.path();
        const destino = join(VID, video + '.webm');
        if (existsSync(destino)) { /* se reemplaza */ }
        renameSync(origen, destino);
        console.log('  video  →', destino.replace(ROOT, '.'));
      }
      await browser.close();
    },
  };
  return api;
}
