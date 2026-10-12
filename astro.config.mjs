import { defineConfig } from 'astro/config';
import rehypeFiguras from './src/lib/rehype-figuras.mjs';

// Sitio 100 % estático. Todo lo que está en public/ se publica tal cual (URLs actuales intactas);
// las páginas nuevas se generan desde src/pages y src/content.
export default defineConfig({
  site: 'https://adestock.com.ar',
  output: 'static',
  trailingSlash: 'ignore',
  build: { format: 'directory', assets: 'assets' },
  markdown: { rehypePlugins: [rehypeFiguras] },
  devToolbar: { enabled: false },
});
