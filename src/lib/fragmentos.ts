import GithubSlugger from 'github-slugger';

export interface Fragmento {
  id: string;
  tutorial_id: string;
  url: string;
  heading_id: string;
  title: string;
  heading: string;
  text: string;
  keywords: string;
  role: string[];
  surface: string[];
  version: string;
  verified_at: string;
}

// Lo mínimo que necesita el índice de cualquier página de ayuda (tutorial o página transversal).
export interface Documento {
  id: string;
  title: string;
  url: string; // ruta base con barra final, ej. /tutoriales/hacer-una-venta/
  body: string;
  synonyms: string[];
  roles: string[];
  surface: string[];
  product_version: string;
  verified_at: string;
}

const MAX_PALABRAS = 220;

function limpiar(md: string): string {
  return md
    .split('\n')
    .filter((l) => !/^\s*\|?[\s:|-]+\|?\s*$/.test(l)) // filas separadoras de tablas
    .map((l) => (l.trim().startsWith('|') ? l.split('|').map((c) => c.trim()).filter(Boolean).join(' · ') : l))
    .join('\n')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/[*_`>]/g, '')
    .replace(/^\s*[-•]\s+/gm, '')
    .replace(/\s+/g, ' ')
    .trim();
}

// Divide el cuerpo por H2/H3 en pasajes de ~100-220 palabras sin partir en medio de un párrafo.
export function fragmentar(doc: Documento): Fragmento[] {
  const slugger = new GithubSlugger(); // mismos ids que genera Astro en los encabezados
  const out: Fragmento[] = [];
  let heading = 'Introducción';
  let headingId = '';
  let parrafos: string[] = [];
  let n = 0;

  const flush = () => {
    const texto = limpiar(parrafos.join('\n\n'));
    parrafos = [];
    if (texto.split(' ').length < 5) return;
    n += 1;
    out.push({
      id: `${doc.id}#${n}`,
      tutorial_id: doc.id,
      url: `${doc.url}${headingId ? '#' + headingId : ''}`,
      heading_id: headingId,
      title: doc.title,
      heading,
      text: texto,
      keywords: doc.synonyms.join(' '),
      role: doc.roles,
      surface: doc.surface,
      version: doc.product_version,
      verified_at: doc.verified_at,
    });
  };

  for (const bloque of (doc.body ?? '').split(/\n{2,}/)) {
    const h = bloque.match(/^(#{2,3})\s+(.*)$/m);
    if (h && bloque.trim().startsWith('#')) {
      flush();
      heading = h[2].replace(/[*_`]/g, '').trim();
      headingId = slugger.slug(heading);
      const resto = bloque.slice(bloque.indexOf('\n') + 1);
      if (bloque.includes('\n') && resto.trim()) parrafos.push(resto);
      continue;
    }
    parrafos.push(bloque);
    if (limpiar(parrafos.join(' ')).split(' ').length >= MAX_PALABRAS) flush();
  }
  flush();
  return out;
}
