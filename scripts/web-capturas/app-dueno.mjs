// Capturas limpias (sin anotaciones) de la app del dueño en formato celular, para la web comercial.
import { abrir } from './_base.mjs';

const c = await abrir({ movil: true });
const p = c.page;
try {
  await c.ir('/app/login/');
  await p.fill('input[name="username"]', 'dueno');
  await p.fill('input[name="password"]', 'demo1234');
  await p.click('button[type="submit"]');
  await c.pausa(1500);

  const pantalla = async (ruta, nombre, { espera = 1200, alto = null } = {}) => {
    await c.ir(ruta);
    await c.pausa(espera);
    // pantalla de celular: se recorta el tamaño visible (390x780 a 2x)
    await c.foto(nombre, alto ? { clip: { x: 0, y: 0, width: 390, height: alto } } : {});
  };

  await pantalla('/app/', 'pwa-inicio');
  await pantalla('/app/radiografia/1/', 'pwa-radiografia', { espera: 2000 });
  await pantalla('/app/productos/', 'pwa-productos');
  await pantalla('/app/cuentas/', 'pwa-cuentas');
  await pantalla('/app/proveedores/', 'pwa-proveedores');
  await pantalla('/app/comparar/', 'pwa-comparar', { espera: 2000 });
} finally {
  await c.cerrar();
}
