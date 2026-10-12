import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const PENDIENTE = 'pendiente-verificar';

// Un tutorial "published" solo compila si pasó revisión: ver superRefine.
const tutoriales = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/tutoriales' }),
  schema: z
    .object({
      id: z.string(),
      slug: z.string().regex(/^[a-z0-9-]+$/),
      title: z.string().min(10),
      description: z.string().min(40).max(200),
      category: z.enum(['empezar', 'vender', 'stock', 'compras', 'clientes', 'ofertas', 'caja', 'instalar']),
      priority: z.enum(['P0', 'P1', 'P2']),
      roles: z.array(z.enum(['dueno', 'cajero', 'administrativo'])).min(1),
      surface: z.array(z.enum(['pos', 'panel', 'app'])).min(1),
      status: z.enum(['draft', 'review', 'published']),
      tiempo: z.string(),
      necesitas: z.string(),
      para_quien: z.string(),
      modulo: z.string(),
      permiso: z.string(),
      source_path: z.string(),
      source_hash: z.string().length(64),
      product_version: z.string(),
      verified_at: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
      reviewed_at: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).nullable(),
      synonyms: z.array(z.string()),
      related: z.array(z.string()),
      social_image: z.string().nullable(),
    })
    .superRefine((t, ctx) => {
      if (t.status !== 'published') return;
      const falta = (campo: string, msg: string) => ctx.addIssue({ code: 'custom', path: [campo], message: msg });
      if (!t.reviewed_at) falta('reviewed_at', 'published exige reviewed_at (revisión editorial)');
      if (t.product_version === PENDIENTE) falta('product_version', 'published exige versión de producto comprobada');
      if (!t.social_image) falta('social_image', 'published exige tarjeta social');
      if (!t.necesitas || !t.permiso) falta('necesitas', 'published exige requisitos y permiso');
    }),
});

export const collections = { tutoriales };
