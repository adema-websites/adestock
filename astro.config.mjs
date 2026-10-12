import { defineConfig } from 'astro/config';
import { existsSync, statSync } from 'node:fs';
import { join } from 'node:path';
import rehypeFiguras from './src/lib/rehype-figuras.mjs';

// Solo desarrollo: nginx sirve /carpeta/ -> /carpeta/index.html desde public/; el dev server de Astro no.
const indicesDePublic = {
  name: 'indices-de-public',
  hooks: {
    'astro:server:setup': ({ server }) => {
      server.middlewares.use((req, _res, next) => {
        const url = (req.url ?? '/').split('?')[0];
        if (url.endsWith('/')) {
          const f = join(process.cwd(), 'public', decodeURIComponent(url), 'index.html');
          if (existsSync(f) && statSync(f).isFile()) req.url = url + 'index.html' + (req.url.includes('?') ? '?' + req.url.split('?')[1] : '');
        }
        next();
      });
    },
  },
};

// Sitio 100 % estático. Todo lo que está en public/ se publica tal cual (URLs actuales intactas);
// las páginas nuevas se generan desde src/pages y src/content.
export default defineConfig({
  site: 'https://adestock.com.ar',
  output: 'static',
  trailingSlash: 'ignore',
  build: { format: 'directory', assets: 'assets' },
  markdown: { rehypePlugins: [rehypeFiguras] },
  integrations: [indicesDePublic],
  devToolbar: { enabled: false },
});
