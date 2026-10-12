import { getCollection, type CollectionEntry } from 'astro:content';
import mapa from '../data/tutoriales-mapa.json';

export type Tutorial = CollectionEntry<'tutoriales'>;

export const SITE = 'https://adestock.com.ar';
export const categorias = mapa.categorias as Record<string, string>;
export const ROLES: Record<string, string> = { dueno: 'Dueño', cajero: 'Cajero', administrativo: 'Administrativo' };
export const SUPERFICIES: Record<string, string> = { pos: 'POS', panel: 'Panel', app: 'App' };

// En dev o con INCLUDE_DRAFTS=1 (staging) se publican también los borradores, siempre con noindex.
export const INCLUDE_DRAFTS = import.meta.env.DEV || process.env.INCLUDE_DRAFTS === '1';

export async function getTutoriales(): Promise<Tutorial[]> {
  const todos = await getCollection('tutoriales');
  const slugs = new Set(todos.map((t) => t.data.slug));
  for (const t of todos) {
    if (t.id !== t.data.slug) throw new Error(`${t.id}: el slug del frontmatter (${t.data.slug}) no coincide con el archivo`);
    for (const r of t.data.related) {
      if (!slugs.has(r)) throw new Error(`${t.id}: related apunta a "${r}", que no existe`);
    }
  }
  const orden = { P0: 0, P1: 1, P2: 2 };
  return todos
    .filter((t) => INCLUDE_DRAFTS || t.data.status === 'published')
    .sort((a, b) => orden[a.data.priority] - orden[b.data.priority] || a.data.title.localeCompare(b.data.title, 'es'));
}

export type Ayuda = CollectionEntry<'ayuda'>;
export async function getAyuda(): Promise<Ayuda[]> {
  const todos = await getCollection('ayuda');
  return todos
    .filter((a) => INCLUDE_DRAFTS || a.data.status === 'published')
    .sort((a, b) => a.data.orden - b.data.orden);
}
export const urlAyuda = (slug: string) => `/ayuda/${slug}/`;

export const esBorrador = (t: Tutorial | Ayuda) => t.data.status !== 'published';
export const urlTutorial = (slug: string) => `/tutoriales/${slug}/`;
