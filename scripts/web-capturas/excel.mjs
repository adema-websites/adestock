// Capturas limpias de la pantalla "Inventario Inicial (Excel)": hasta la vista previa, SIN confirmar la importación.
import { join } from 'node:path';
import { abrir, ROOT } from './_base.mjs';

const OUT = join(ROOT, 'src', 'assets', 'web-excel');
const ARCHIVO = join(ROOT, 'docs', 'ejemplos', 'productos-ejemplo.xlsx');
const c = await abrir({ ancho: 1366, alto: 800 });
const p = c.page;
try {
  await c.login();
  await c.ir('/admin/inventario-inicial/');
  await c.pausa(1500);
  console.log('url', p.url());
  await p.locator('.content-wrapper, main, #content').first().screenshot({ path: join(OUT, '01-pantalla.png') }).catch(() => p.screenshot({ path: join(OUT, '01-pantalla.png'), fullPage: true }));
  await p.setInputFiles('input[type=file]', ARCHIVO);
  await c.pausa(500);
  await p.locator('form:has(input[type=file]) button[type=submit], form:has(input[type=file]) input[type=submit]').first().click();
  await c.pausa(2500);
  const prev = p.locator('div.module:has(h2:has-text("Preview de cambios"))').last();
  await prev.scrollIntoViewIfNeeded();
  await prev.screenshot({ path: join(OUT, '03-vista-previa.png') });
  const resumen = p.locator('div.module:has(fieldset.module)').first();
  await resumen.screenshot({ path: join(OUT, '04-resumen.png') }).catch(() => {});
  console.log(await p.evaluate(() => document.body.innerText.replace(/\s+/g, ' ').slice(0, 900)));
} finally {
  await c.cerrar();
}
