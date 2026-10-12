# Tienda de temas de revistas en adestock.com.ar

> **Estado:** diseño acordado el 2026-10-10, **nada implementado**. Este documento es el contrato entre
> la web (adestock.com.ar) y el sistema Adestock (app `publicaciones`, POS → Revistas y folletos).
> **Para quién:** quien arme la web y cargue los temas. No hace falta conocer el código del sistema.

## 1. Qué se quiere lograr

- Publicar en adestock.com.ar una galería de **temas gratuitos** para las revistas y folletos del POS.
- Cada tema es un **ZIP** que se puede descargar a mano e importar, **o** instalarse con un clic desde
  dentro del Adestock ("Explorar temas online").
- Más adelante algunos temas podrán ser **premium** (pagos). El formato ya lo prevé; hoy todos son gratis.
- Modelo a copiar: las skins de la tienda online del propio Adestock y la tienda de skins de SistemaBurger.

## 2. Qué tiene que ofrecer la web

Son dos cosas: un **índice** (JSON) y los **ZIP**. Alcanza con archivos estáticos; no hace falta backend ni usuarios.

```
https://adestock.com.ar/api/temas-revista/index.json        lista de temas
https://adestock.com.ar/api/temas-revista/<id>/<id>-<version>.zip   el tema
https://adestock.com.ar/api/temas-revista/<id>/miniatura.webp       vista previa (tarjeta)
https://adestock.com.ar/api/temas-revista/<id>/vista-1.webp ...     capturas (opcional, hasta 4)
```

Además, una página pública (por ejemplo `adestock.com.ar/temas-revistas/`) con las mismas tarjetas y un botón
"Descargar ZIP", para quien quiera bajarlo e importarlo a mano. **No usar la URL `/revista/`**: es la de la
tienda online del sistema.

Requisitos del servidor: HTTPS obligatorio, `Content-Type` correcto (`application/json`, `application/zip`),
cabecera `Cache-Control` corta para el índice (por ejemplo 5 minutos) y larga para los ZIP versionados.

### 2.1 `index.json`

```json
{
  "formato": 1,
  "actualizado": "2026-10-10T20:00:00-03:00",
  "temas": [
    {
      "id": "navidad-dorado",
      "nombre": "Navidad dorado",
      "descripcion": "Fondo verde oscuro con detalles dorados para ofertas de fin de año.",
      "autor": "ADEMA Sistemas",
      "version": "1.0.0",
      "premium": false,
      "etiquetas": ["navidad", "fiestas", "oscuro"],
      "formatos": ["a4", "a4h", "post", "postv", "historia"],
      "miniatura": "navidad-dorado/miniatura.webp",
      "capturas": ["navidad-dorado/vista-1.webp"],
      "zip": "navidad-dorado/navidad-dorado-1.0.0.zip",
      "bytes": 482113,
      "sha256": "9f2c…(64 caracteres hexadecimales)",
      "requiere_formato": 1,
      "publicado": "2026-10-10"
    }
  ]
}
```

Reglas del índice:

- `id`: minúsculas, números y guiones (`^[a-z0-9]+(-[a-z0-9]+)*$`), único y **nunca se reutiliza**.
- `version`: `MAYOR.MENOR.PARCHE`. Cada cambio del ZIP sube la versión y genera un archivo nuevo; el sistema
  usa esto para avisar "hay una versión nueva".
- `bytes` y `sha256`: del ZIP exacto. El sistema los verifica antes de instalar; si no coinciden, rechaza.
- `premium`: `false` por ahora. Cuando exista un tema pago, el sistema mostrará un candado y pedirá licencia
  (esa parte se definirá después; **no construir nada de cobro todavía**).
- `requiere_formato`: versión del formato de ZIP (sección 3). Si el sistema es más viejo, no ofrece el tema.
- Las rutas (`miniatura`, `zip`, `capturas`) son **relativas** al directorio del índice. El sistema ignora
  cualquier URL absoluta o de otro dominio.
- `miniatura`: WebP, 600 × 424 px aprox., hasta 150 KB. Conviene que sea una captura real de una hoja A4.

## 3. El ZIP de un tema

Archivos en la **raíz** del ZIP (el sistema también tolera que estén dentro de una única carpeta):

```
tema.json                  obligatorio
tema.css                   opcional   retoques de estilo (validado, ver 3.2)
fondo.webp|png|jpg|svg     opcional   imagen de fondo de la hoja
vista-previa.webp          opcional   captura (se ignora al importar)
INSTRUCCIONES-PARA-IA.md   opcional   guía para pedirle variantes a una IA (se ignora al importar)
```

Se ignoran sin error los archivos que no forman parte del formato. Nunca se ejecuta ni se guarda nada que no sea
`tema.json`, `tema.css` y `fondo.*`.

### 3.1 `tema.json`

```json
{
  "formato": 1,
  "producto": "adestock-revista-tema",
  "id": "navidad-dorado",
  "nombre": "Navidad dorado",
  "descripcion": "Fondo verde oscuro con detalles dorados.",
  "autor": "ADEMA Sistemas",
  "version": "1.0.0",
  "base": "oscuro",
  "valores": {
    "colores": {
      "fondo": "#0b3d2e",
      "cabecera_fondo": "#0b3d2e",
      "cabecera_texto": "#ffffff",
      "titulo": "#f5c542",
      "tarjeta": "#fffaf0",
      "texto": "#1b1b1b",
      "texto_suave": "#5c5c5c",
      "precio": "#b3122a",
      "promo": "#0b3d2e",
      "sello_fondo": "#b3122a",
      "sello_texto": "#ffffff",
      "franja_fondo": "#f5c542",
      "franja_texto": "#0b3d2e",
      "vigencia_fondo": "#f5c542",
      "vigencia_texto": "#0b3d2e",
      "pie_fondo": "#072a20",
      "pie_texto": "#e8e0c8"
    },
    "fuente_titulo": "fraunces",
    "fuente_texto": "barlow",
    "fuente_precio": "archivo",
    "radio_tarjeta": 14,
    "forma_sello": "circulo",
    "sello_inclinado": true,
    "sombra": true,
    "fondo_velo": 20
  },
  "fondo": { "archivo": "fondo.webp" }
}
```

Valores permitidos (todo lo que no figure acá, el sistema lo **rechaza** con un mensaje claro):

| Campo | Valores válidos |
|---|---|
| `base` | `super`, `oscuro`, `minimal`, `verano` (tema incluido del que hereda la estructura) |
| `colores.*` | `#rrggbb` (6 dígitos). Claves: `fondo`, `cabecera_fondo`, `cabecera_texto`, `titulo`, `tarjeta`, `texto`, `texto_suave`, `precio`, `promo`, `sello_fondo`, `sello_texto`, `franja_fondo`, `franja_texto`, `vigencia_fondo`, `vigencia_texto`, `pie_fondo`, `pie_texto`. Las que falten toman el color del tema `base`. |
| `fuente_titulo`, `fuente_texto`, `fuente_precio` | `archivo` (Archivo Black), `barlow-cond` (Barlow Condensed), `barlow` (Barlow), `baloo` (Baloo 2), `fraunces` (Fraunces). **Solo estas cinco**: vienen incluidas en el sistema, que corre sin internet. |
| `radio_tarjeta` | entero de 0 a 30 (px) |
| `forma_sello` | `circulo`, `cuadrado`, `pastilla` |
| `sello_inclinado`, `sombra` | `true` / `false` |
| `fondo_velo` | entero de 0 a 80 (% del color de fondo sobre la imagen) |

> Si hace falta una tipografía nueva, hay que agregarla al sistema (viaja en su instalador); un ZIP no puede
> traer fuentes.

### 3.2 `tema.css` (opcional, validado)

Sirve para lo que los parámetros no alcanzan: banda de precio, olas, guirnaldas, bordes, sellos con forma propia.

**Cómo se aplica:** el sistema antepone `.hoja[data-tema="…"]` a **cada** regla. El CSS de un tema nunca puede
afectar nada fuera de la hoja de la revista.

**Selectores permitidos** (solo clases de la hoja; sin ids, etiquetas sueltas, atributos ni `*`):

`.hoja`, `.h-cab`, `.h-marca`, `.h-logo`, `.h-titulos`, `.h-titulo`, `.h-vig`, `.h-cuerpo`, `.h-pie`, `.ribbon`,
`.seccion`, `.grilla`, `.card`, `.foto`, `.sello`, `.info`, `.nombre`, `.pres`, `.precio-zona`, `.antes`,
`.precio`, `.etq-precio`, `.leyenda-promo`, `.extra`, `.dia`, `.hero`, `.hero-card`, `.hero-info`, `.portada`,
`.portada-titulo`, `.portada-sub`. Se admiten combinadores (espacio, `>`), `:first-child`, `:last-child`,
`:nth-child()`, `::before` y `::after`.

**Propiedades permitidas:** colores y fondos (`color`, `background`, `background-color`, `background-image`
solo con gradientes, `background-size`, `background-position`, `background-repeat`), bordes (`border*`,
`border-radius`, `outline`), sombras (`box-shadow`, `text-shadow`, `filter: drop-shadow()`), tipografía
(`font-weight`, `font-style`, `letter-spacing`, `text-transform`, `text-shadow`, `line-height`, `text-align`),
espaciado (`padding*`, `margin*`, `gap`), tamaño (`width`, `height`, `min-*`, `max-*`, `aspect-ratio`),
`transform` (rotate, scale, translate), `opacity`, `content` (solo texto corto, para `::before`/`::after`),
y las variables `--t-*`.

**Reglas de contenido:**

- Prohibido: `url()` (las imágenes viajan como `fondo.*`), `@import`, `@font-face`, `@media`, `@keyframes`,
  `!important`, `expression()`, `behavior`, `javascript:`, `position: fixed`, `position: absolute` fuera de
  `::before`/`::after`, `z-index` mayores a 5.
- Permitido: gradientes (`linear-gradient`, `radial-gradient`, `repeating-linear-gradient`), `calc()`, `var()`,
  `rgba()`, `rotate()`, `scale()`.
- Tamaño máximo: 50.000 bytes, UTF-8.
- **Unidades:** la hoja se escala sola, así que usá `cqw`, `cqmin` y `cqh` (como en el sistema), no `px` para
  tamaños de letra. El A4 mide 794 × 1123 px y las piezas de redes 1080 px de ancho.
- Probar siempre el tema en **los 5 formatos** (A4, A4 horizontal, post, post vertical, historia).

**Mejor práctica:** usá `var(--t-…)` para colores en vez de repetir hexadecimales; así el tema sigue
funcionando si el usuario cambia un color desde el editor de temas del sistema. Variables disponibles:
`--t-bg`, `--t-ink`, `--t-muted`, `--t-card`, `--t-radius`, `--t-card-shadow`, `--t-card-border`, `--t-head-bg`,
`--t-head-fg`, `--t-title`, `--t-cover-title`, `--t-logo-bg`, `--t-logo-fg`, `--t-vig-bg`, `--t-vig-fg`,
`--t-pie-bg`, `--t-pie-fg`, `--t-ribbon-bg`, `--t-ribbon-fg`, `--t-ribbon-radius`, `--t-sello-bg`,
`--t-sello-fg`, `--t-sello-radius`, `--t-sello-rot`, `--t-sello-shadow`, `--t-sello-border`, `--t-precio`,
`--t-promo`, `--t-precio-bg`, `--t-precio-pad`, `--t-precio-radius`, `--t-f-display`, `--t-f-body`,
`--t-f-price`, `--t-name-case`, `--t-title-track`, `--t-price-track`.

### 3.3 Fondo

- Extensiones: `.webp`, `.png`, `.jpg`, `.jpeg`, `.svg`. Hasta 5 MB.
- SVG: simple, sin `<script>`, sin `href`/`xlink:href` externos, sin `<foreignObject>`, sin `<image>` a otra URL.
- Se ajusta para cubrir la hoja. Una imagen apaisada se ve mal estirada en una historia vertical:
  conviene un fondo pensado para el formato más usado o un diseño que admita recorte.
- Tamaño recomendado para impresión A4: 1588 × 2246 px (≈200 dpi). Para redes, 1080 × 1920 px.

### 3.4 Límites generales

ZIP máximo 8 MB, sin contraseña, sin enlaces simbólicos, rutas sin `..`, `\` ni `:`, máximo 20 archivos.

## 4. Qué hace el sistema Adestock con esto

Esto lo construye el equipo del sistema; está acá para que la web sepa qué se espera.

1. El **servidor del Adestock** (no el navegador) pide `index.json`. Dominio fijo `adestock.com.ar`, solo HTTPS,
   timeout corto y tope de tamaño. Si no hay internet muestra "sin conexión" y ofrece importar un ZIP a mano.
2. Muestra la galería con miniaturas, etiquetas y "Instalar" / "Actualizar" / "Instalado".
3. Al instalar descarga el ZIP, verifica `bytes` y `sha256`, pasa por el **mismo validador** que la importación
   manual y guarda el tema como "tema propio" con `origen = online`, `id_remoto` y `version`.
4. El tema instalado queda disponible en el selector de Tema de las revistas. Importar nunca pisa un tema
   existente sin avisar; una versión nueva se instala como actualización explícita.
5. Una revista **publicada** guarda una copia del tema al publicarse, para que no cambie si después se borra
   o actualiza el tema (pendiente de definir en el sistema).

## 5. Cómo cargar un tema nuevo en la web (procedimiento)

1. Armar `tema.json` (y `tema.css`, `fondo.*` si corresponde). Se puede partir de un ZIP exportado desde el
   propio Adestock ("Exportar tema") o pedirle a una IA que lo cree con `INSTRUCCIONES-PARA-IA.md`.
2. **Importarlo en un Adestock de pruebas** y verificar los 5 formatos con productos reales y sin foto,
   con 1, 5 y 30 productos, y con precios largos (`$ 112.450,00`).
3. Sacar la miniatura y las capturas.
4. Armar el ZIP final (`<id>-<version>.zip`), calcular el hash: `sha256sum <id>-<version>.zip`
   (PowerShell: `Get-FileHash <archivo> -Algorithm SHA256`).
5. Subir el ZIP, la miniatura y las capturas a `/api/temas-revista/<id>/`.
6. Agregar el tema a `index.json` con `bytes` y `sha256`, y actualizar `actualizado`.
7. Comprobar desde un Adestock real: aparece en la galería, se instala y se ve igual que en las pruebas.

Para retirar un tema: sacarlo del índice (los ya instalados siguen funcionando). Para corregirlo: subir una
versión nueva, **nunca reemplazar un ZIP ya publicado** (rompería el `sha256`).

## 6. Seguridad (resumen)

- Un tema es **datos más CSS acotado**: nunca HTML ni JavaScript.
- Todo se valida en el sistema, aunque venga de la web oficial. Un tema inválido se rechaza completo y no
  deja nada guardado a medias.
- Sin `url()` en el CSS, sin recursos externos, sin fuentes externas: la revista se exporta igual sin internet
  y sin filtrar datos.
- La web no recibe nada del sistema: no se envían datos del comercio, productos ni precios. A lo sumo el
  sistema consulta el índice y descarga archivos públicos.

## 7. Pendientes y decisiones abiertas

- Cómo está montada adestock.com.ar (estático, Django u otro): define si `index.json` se genera solo a partir
  de una carpeta de temas o se edita a mano.
- Temas premium: cómo se valida la licencia al descargar (se reutilizaría el sistema de licencias del Adestock).
- Un fondo distinto por formato (A4 vs. historia vertical): posible segunda versión del formato.
- Contador de descargas / valoraciones: no incluido; se puede sumar después sin cambiar el formato.
- Qué hacer si un tema depende de una fuente que aún no viene en el sistema (hoy: no se admite).
