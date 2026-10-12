// POS con un carrito armado y pantalla de cobro. Capturas limpias para el circuito diario.
import { abrir } from './_base.mjs';

const c = await abrir({ ancho: 1440, alto: 900 });
const p = c.page;
const agregar = async (texto, indice = 0) => {
  for (let i = 0; i < 4; i++) {
    await p.fill('#search-product', texto);
    await c.pausa(2000);
    try {
      const b = p.locator('.producto-sugerencia .precio-btn-sug').nth(indice);
      await b.waitFor({ state: 'visible', timeout: 4000 });
      await b.click({ timeout: 4000 });
      await c.pausa(1300);
      return;
    } catch { await c.pausa(800); }
  }
  throw new Error('no se pudo agregar ' + texto);
};
try {
  await c.login();
  await c.abrirTurno();
  await c.ir('/pos/');
  await c.pausa(1500);
  await p.click('#btn-vaciar-carrito').catch(() => {});
  await c.pausa(1200);
  await agregar('Yerba');
  await agregar('Aceite');
  await agregar('Fideos');
  await agregar('Gaseosa Cola 2.25');
  await p.fill('#search-product', '');
  await c.pausa(1000);
  await c.foto('pos-carrito');
} finally {
  await c.cerrar();
}
