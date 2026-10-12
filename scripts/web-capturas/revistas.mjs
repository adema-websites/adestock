// Flujo de revistas: de las ofertas a la revista armada. Graba video y deja capturas limpias.
import { abrir } from './_base.mjs';

const c = await abrir({ video: 'revista-flujo' });
const p = c.page;
try {
  await c.login();
  await c.abrirTurno();
  await c.ir('/pos/publicaciones/');
  await c.pausa(1500);
  await c.foto('revistas-listado');

  await p.click('#nueva');
  await c.pausa(1500);
  await p.fill('#f-nombre', 'Ofertas de la semana');
  await p.selectOption('#f-columnas', '2');
  await p.selectOption('#f-filas', '3');
  await p.click('button:has-text("ADE Bauhaus")');
  await c.pausa(700);
  await c.foto('revistas-editor');

  await p.click('#traer-ofertas');
  await c.pausa(2500);
  await p.click('#abrir-catalogo');
  await c.pausa(1500);
  await p.fill('dialog input[type="search"], dialog input[type="text"], [role=dialog] input', 'Yerba').catch(() => {});
  await c.pausa(1500);
  await p.locator('.pres-btn').nth(1).click().catch(() => {});
  await c.pausa(700);
  await p.locator('.pres-btn').nth(0).click().catch(() => {});
  await c.pausa(700);
  await p.click('button:has-text("Listo")').catch(() => {});
  await c.pausa(2200);
  await c.foto('revistas-armada');

  await p.click('#guardar');
  await c.pausa(2000);
  await p.click('#exportar').catch(() => {});
  await c.pausa(1800);
  await c.foto('revistas-exportar');
} finally {
  await c.cerrar();
}
