// Publica (o retira) guías. Es el único paso que marca una guía como revisada: lo ejecuta una persona.
// Uso:
//   node scripts/publicar_guias.mjs --revisor "Kevin" --todas
//   node scripts/publicar_guias.mjs --revisor "Kevin" hacer-una-venta,contar-stock
//   node scripts/publicar_guias.mjs --retirar hacer-una-venta
// Exige, por guía: product_version comprobada y tarjeta social (genera el build si falta algo).
import { readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const val = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const revisor = val('--revisor');
const retirar = val('--retirar');
const todas = args.includes('--todas');
const slugs = args.filter((a, i) => !a.startsWith('--') && !['--revisor', '--retirar'].includes(args[i - 1]));
const lista = retirar ? retirar.split(',') : todas ? null : (slugs[0] ?? '').split(',').filter(Boolean);

if (!retirar && !revisor) { console.error('Falta --revisor "Nombre": quién revisó las guías.'); process.exit(1); }
if (!retirar && !todas && !lista.length) { console.error('Indicá --todas o una lista de slugs.'); process.exit(1); }

const hoy = new Date().toISOString().slice(0, 10);
const carpetas = [join(ROOT, 'src', 'content', 'tutoriales'), join(ROOT, 'src', 'content', 'ayuda')];
let cambiadas = 0;
const omitidas = [];

for (const dir of carpetas) {
  if (!existsSync(dir)) continue;
  for (const f of readdirSync(dir).filter((x) => x.endsWith('.md'))) {
    const slug = f.replace(/\.md$/, '');
    if (lista && !lista.includes(slug)) continue;
    const ruta = join(dir, f);
    let s = readFileSync(ruta, 'utf8');
    const campo = (k) => (s.match(new RegExp(`^${k}: (.*)$`, 'm')) ?? [])[1];
    if (retirar) {
      s = s.replace(/^status: .*$/m, 'status: "draft"').replace(/^reviewed_at: .*$/m, 'reviewed_at: null');
    } else {
      // Las páginas de ayuda general usan la tarjeta del centro de ayuda.
      if (dir.endsWith('ayuda') && JSON.parse(campo('social_image') ?? 'null') === null) {
        s = s.replace(/^social_image: .*$/m, 'social_image: "/social/tutoriales-v1.jpg"');
      }
      const falta = [];
      if (JSON.parse(campo('product_version') ?? '""') === 'pendiente-verificar') falta.push('product_version');
      if (JSON.parse(campo('social_image') ?? 'null') === null) falta.push('social_image');
      if (falta.length) { omitidas.push(`${slug}: falta ${falta.join(', ')}`); continue; }
      s = s.replace(/^status: .*$/m, 'status: "published"').replace(/^reviewed_at: .*$/m, `reviewed_at: "${hoy}"`);
      if (/^reviewed_by: /m.test(s)) s = s.replace(/^reviewed_by: .*$/m, `reviewed_by: ${JSON.stringify(revisor)}`);
      else s = s.replace(/^(reviewed_at: .*)$/m, `$1\nreviewed_by: ${JSON.stringify(revisor)}`);
    }
    writeFileSync(ruta, s);
    cambiadas++;
  }
}
console.log(`${retirar ? 'Retiradas' : 'Publicadas'}: ${cambiadas}`);
if (omitidas.length) console.log('Omitidas:\n  ' + omitidas.join('\n  '));
