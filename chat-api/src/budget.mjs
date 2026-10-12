// Tope de gasto mensual persistido en disco (un archivo por mes). Estima el costo con los tokens
// que informa Gemini (usageMetadata). Los precios son configurables: verificarlos en la tarifa vigente de Google.
import { mkdirSync, readFileSync, writeFileSync, renameSync } from 'node:fs';
import { join } from 'node:path';

export function crearPresupuesto({ dir, limiteUsd, precioEntradaPorM, precioSalidaPorM, ahora = () => new Date() }) {
  mkdirSync(dir, { recursive: true });
  const archivo = () => join(dir, `gasto-${ahora().toISOString().slice(0, 7)}.json`);

  const leer = () => {
    try { return JSON.parse(readFileSync(archivo(), 'utf8')); } catch { return { usd: 0, consultas: 0 }; }
  };
  const guardar = (d) => {
    const tmp = archivo() + '.tmp';
    writeFileSync(tmp, JSON.stringify(d));
    renameSync(tmp, archivo());
  };

  return {
    gastado: () => leer().usd,
    limite: limiteUsd,
    // Peor caso razonable por consulta: antes de llamar, se exige margen para no pasarse del tope.
    agotado(reservaUsd = 0) { return leer().usd + reservaUsd >= limiteUsd; },
    registrar({ tokensEntrada = 0, tokensSalida = 0 }) {
      const costo = (tokensEntrada / 1e6) * precioEntradaPorM + (tokensSalida / 1e6) * precioSalidaPorM;
      const d = leer();
      d.usd = Number((d.usd + costo).toFixed(6));
      d.consultas += 1;
      guardar(d);
      return costo;
    },
    resumen() { const d = leer(); return { mes: ahora().toISOString().slice(0, 7), ...d, limiteUsd }; },
  };
}
