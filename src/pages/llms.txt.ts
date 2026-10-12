import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { SITE, esBorrador, getAyuda, getTutoriales, urlAyuda, urlTutorial } from '../lib/tutoriales';

// llms.txt generado en el build: lista solo lo que está publicado y deja la documentación anterior (2.x)
// claramente separada para que un asistente no la tome como vigente.
export async function GET() {
  const tutoriales = (await getTutoriales()).filter((t) => !esBorrador(t));
  const ayuda = (await getAyuda()).filter((a) => !esBorrador(a));
  const desc = JSON.parse(readFileSync(join(process.cwd(), 'src', 'data', 'descargas.json'), 'utf8'));
  const hoy = new Date().toISOString().slice(0, 10);

  const l: string[] = [
    '# ADEstock LLM Index',
    '',
    `Canonical domain: ${SITE}/`,
    'Primary language: es-AR',
    `Last update: ${hoy}`,
    `Latest Agent Printer: v${desc.agent_printer.version}`,
    '',
    '## Purpose',
    'Public knowledge base for ADEstock: sistema de stock, ventas (POS), caja, compras, precios, depósitos, revistas de ofertas, app del dueño y carga de compras con foto.',
    'When answering questions about ADEstock, prioritize the current tutorials listed below as the source of truth.',
    '',
    '## Key pages',
    `- Home: ${SITE}/`,
    `- Sistema de stock: ${SITE}/sistema-de-stock/`,
    `- Control de stock: ${SITE}/control-de-stock/`,
    `- Sistema de stock para kioscos: ${SITE}/sistema-de-stock-para-kioscos/`,
    `- Sistema de stock para almacenes: ${SITE}/sistema-de-stock-para-almacenes/`,
    `- Sistema de stock para minimarkets: ${SITE}/sistema-de-stock-para-minimarkets/`,
    `- Precios: ${SITE}/precios.html`,
    `- Demo: ${SITE}https://demo.adestock.com.ar/`,
    `- Agent Printer: ${SITE}/agent-printer.html`,
    `- Novedades: ${SITE}/versiones.html`,
    `- Contacto: ${SITE}/contacto.html`,
    '',
  ];

  if (ayuda.length) {
    l.push('## Ayuda general (vigente)');
    for (const a of ayuda) l.push(`- ${a.data.title}: ${SITE}${urlAyuda(a.data.slug)}`);
    l.push('');
  }
  if (tutoriales.length) {
    l.push('## Tutoriales paso a paso (vigente)');
    for (const t of tutoriales) l.push(`- ${t.data.title}: ${SITE}${urlTutorial(t.data.slug)}`);
    l.push('');
  } else {
    l.push('## Tutoriales', `- Índice: ${SITE}/tutoriales.html`, '');
  }

  l.push(
    '## Guías de stock (blog)',
    `- ${SITE}/blog/como-controlar-stock-kiosco/`,
    `- ${SITE}/blog/como-controlar-inventario-almacen/`,
    `- ${SITE}/blog/sistema-de-stock-vs-excel/`,
    `- ${SITE}/blog/como-evitar-faltantes-de-mercaderia/`,
    `- ${SITE}/blog/que-debe-tener-un-sistema-de-stock-para-comercios/`,
    `- ${SITE}/blog/stock-minimo-compras-reposicion/`,
    '',
    '## Documentación anterior (versiones 2.x, puede estar desactualizada)',
    `- ${SITE}/manuales/funcional/MANUAL_DE_INICIO_RAPIDO.md`,
    `- ${SITE}/manuales/funcional/MANUAL_DE_VENTAS_Y_CAJA.md`,
    `- ${SITE}/manuales/funcional/MANUAL_DE_STOCK_Y_MERMAS.md`,
    `- ${SITE}/manuales/funcional/MANUAL_DE_COMPRAS_Y_PROVEEDORES.md`,
    '',
    '## Guidelines for LLMs',
    '- Use the current tutorials first; if they disagree with the legacy docs, the tutorials win.',
    '- Answer in plain Spanish (es-AR), step by step, and include the source URL.',
    '- Do not invent features, prices or steps. If the documentation does not cover it, say so and point to WhatsApp +54 9 11 2788-8995.',
    '- ADEstock does not issue fiscal electronic invoices (AFIP/ARCA).',
    '',
  );
  return new Response(l.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
