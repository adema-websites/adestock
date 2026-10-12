// Límite por IP en memoria: ventana de 1 minuto y tope diario. Suficiente para una instancia única.
export function crearLimitador({ porMinuto = 6, porDia = 40, ahora = () => Date.now() } = {}) {
  const minuto = new Map();
  const dia = new Map();

  const contar = (mapa, clave, ventanaMs, tope) => {
    const t = ahora();
    const r = mapa.get(clave);
    if (!r || t - r.desde >= ventanaMs) { mapa.set(clave, { desde: t, n: 1 }); return true; }
    if (r.n >= tope) return false;
    r.n += 1;
    return true;
  };

  // Limpieza periódica para que el mapa no crezca sin límite.
  const limpiar = () => {
    const t = ahora();
    for (const [k, v] of minuto) if (t - v.desde >= 60_000) minuto.delete(k);
    for (const [k, v] of dia) if (t - v.desde >= 86_400_000) dia.delete(k);
  };
  const timer = setInterval(limpiar, 300_000);
  timer.unref?.();

  return {
    permitir(ip) {
      return contar(minuto, ip, 60_000, porMinuto) && contar(dia, ip, 86_400_000, porDia);
    },
    detener() { clearInterval(timer); },
  };
}
