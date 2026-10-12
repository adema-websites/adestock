import { defineConfig } from 'astro/config';

// Sitio 100 % estático. Todo lo que está en public/ se publica tal cual (URLs actuales intactas);
// las páginas nuevas se generan desde src/pages y src/content.
export default defineConfig({
  site: 'https://adestock.com.ar',
  output: 'static',
  trailingSlash: 'ignore',
  build: { format: 'preserve' },
  devToolbar: { enabled: false },
});
