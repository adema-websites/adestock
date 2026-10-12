import { getAyuda, getTutoriales, urlAyuda, urlTutorial } from '../../lib/tutoriales';
import { fragmentar, type Documento } from '../../lib/fragmentos';
import sinonimos from '../../data/sinonimos.json';

// Índice del buscador y del chat, generado en el build. Solo contenido que se publica
// (en staging con INCLUDE_DRAFTS=1 también los borradores).
export async function GET() {
  const tutoriales = await getTutoriales();
  const ayuda = await getAyuda();
  const docs: Documento[] = [
    ...tutoriales.map((t) => ({
      id: t.data.id, title: t.data.title, url: urlTutorial(t.data.slug), body: t.body ?? '',
      synonyms: t.data.synonyms, roles: t.data.roles, surface: t.data.surface,
      product_version: t.data.product_version, verified_at: t.data.verified_at,
    })),
    ...ayuda.filter((a) => a.data.slug !== 'preguntas-frecuentes').map((a) => ({ // la FAQ repite los "Problemas frecuentes" de cada guía: se excluye para no taparlas
      id: a.data.id, title: a.data.title, url: urlAyuda(a.data.slug), body: a.body ?? '',
      synonyms: a.data.synonyms, roles: ['dueno', 'cajero', 'administrativo'], surface: ['pos', 'panel', 'app'],
      product_version: a.data.product_version, verified_at: a.data.verified_at,
    })),
  ];
  const { _nota, ...sin } = sinonimos as Record<string, string>;
  return new Response(JSON.stringify({ fragmentos: docs.flatMap(fragmentar), sinonimos: sin }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
