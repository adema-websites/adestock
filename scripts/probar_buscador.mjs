// Evalúa el buscador contra el banco de consultas. Requiere un build con borradores:
//   INCLUDE_DRAFTS=1 npm run build && node scripts/probar_buscador.mjs
// Criterio del plan: >=90 % de consultas con el tutorial correcto entre los 3 primeros y las críticas en el 1.º lugar.
import { readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import MiniSearch from 'minisearch';
import { buscar, opcionesMiniSearch } from '../src/lib/buscador-config.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const { fragmentos, sinonimos } = JSON.parse(readFileSync(join(ROOT, 'dist', 'tutoriales', 'indice.json'), 'utf8'));
const { consultas } = JSON.parse(readFileSync(join(ROOT, 'src', 'data', 'consultas-prueba.json'), 'utf8'));
const ms = new MiniSearch(opcionesMiniSearch);
ms.addAll(fragmentos);

let top1 = 0, top3 = 0, critTotal = 0, critOk = 0;
const fallos = [];
for (const c of consultas) {
  const r = buscar(ms, c.q, sinonimos).map((g) => g.tutorial_id);
  const pos = r.indexOf(c.esperado);
  if (pos === 0) top1++;
  if (pos >= 0 && pos < 3) top3++;
  if (c.critica) { critTotal++; if (pos === 0) critOk++; }
  if (pos !== 0) fallos.push(`  ${pos < 0 ? 'NO ESTÁ' : 'puesto ' + (pos + 1)}  «${c.q}» → esperado ${c.esperado}; devolvió ${r.slice(0, 3).join(', ') || '(nada)'}`);
}
const n = consultas.length;
console.log(`Fragmentos: ${fragmentos.length}  |  Consultas: ${n}`);
console.log(`Primer lugar: ${top1}/${n}  |  Entre los 3 primeros: ${top3}/${n} (${Math.round((top3 / n) * 100)} %)  |  Críticas en 1.º: ${critOk}/${critTotal}`);
if (fallos.length) console.log('\nNo acertaron en 1.º lugar:\n' + fallos.join('\n'));
const ok = top3 / n >= 0.9 && critOk === critTotal;
console.log(`\n${ok ? 'CUMPLE' : 'NO CUMPLE'} el criterio de aceptación`);
process.exitCode = ok ? 0 : 1;
