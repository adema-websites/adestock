import { getTutoriales } from '../../lib/tutoriales';
import { fragmentar } from '../../lib/fragmentos';
import sinonimos from '../../data/sinonimos.json';

// Índice del buscador, generado en el build. Un fragmento por pasaje; solo contenido que se publica.
export async function GET() {
  const todos = await getTutoriales();
  const fragmentos = todos.flatMap(fragmentar);
  const { _nota, ...sin } = sinonimos as Record<string, string>;
  return new Response(JSON.stringify({ fragmentos, sinonimos: sin }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
