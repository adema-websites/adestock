# Panel de temas de revista (solo administrador)

Implementa el contrato de `../../docs/README_WEB_TIENDA_TEMAS_REVISTAS.md`.

**Arquitectura:** la web pública sigue siendo 100 % estática (`public/api/temas-revista/`, `public/temas-revistas/`). Este panel es una
app Flask que corre **solo en tu PC** (`127.0.0.1`), valida, calcula la huella, firma y escribe en `api/temas-revista/`.
Vos hacés `git commit` + `git push`. Ningún endpoint público acepta subidas porque en el servidor no hay nada que ejecutar.

> Esta carpeta está dentro del repo, fuera de `public/` (no se publica), y **no contiene secretos**: contraseña, 2FA, clave de firma,
> auditoría y backups viven en el directorio de estado, **fuera del repo**:
> Windows `%LOCALAPPDATA%\adestock-temas-admin`, Linux/Mac `~/.adestock-temas-admin` (o `ADESTOCK_TEMAS_ESTADO`).
> `catalogo.json` es la fuente de verdad (versiones, huellas, retirados); se versiona con git.

## Instalación (una vez)

```powershell
cd tools/admin-temas
pip install -r requirements.txt
python -m adestock_temas init
```

`init` te pide una contraseña (≥14 caracteres, 3 tipos), crea el secreto 2FA (cargalo en tu app TOTP) y genera la
clave de firma Ed25519, **cifrada con tu contraseña**. Imprime la clave pública para incrustar en el Adestock.

## Cargar un tema nuevo o una versión nueva

1. Armá el ZIP (`tema.json` + opcionalmente `tema.css`, `fondo.*`…) y probalo en un Adestock de pruebas (5 formatos).
2. Sacá la miniatura WebP (600×424 aprox., ≤150 KB) y hasta 4 capturas WebP.
3. `python -m adestock_temas panel` → abrí <http://127.0.0.1:8765> → contraseña + código 2FA.
4. **Subir tema / versión**: elegí ZIP, miniatura (obligatoria en un tema nuevo), capturas, etiquetas y formatos.
   `premium` queda sin marcar. El id, nombre y versión salen del `tema.json`.
5. Si se rechaza, se listan todos los motivos. Si pasa, ves id, versión, tamaño y **sha256 calculados** y la miniatura.
6. Repetí tu contraseña y **Publicar y firmar índice**. Se escriben el ZIP (nunca reemplaza uno existente), las imágenes,
   `catalogo.json`, `index.json` e `index.json.sig`.
7. `git add public/api tools/admin-temas/catalogo.json && git commit -m "Tema X vX.Y.Z" && git push`
8. Comprobá `https://adestock.com.ar/api/temas-revista/index.json` y `/temas-revistas/`; en el panel, **Verificar**.

Para corregir un tema: subí una versión **mayor** (el id no cambia). Para retirarlo: pantalla del tema → *Retirar*
(sale del índice; los ZIP no se borran; se puede *Restaurar*). `premium`, etiquetas y formatos se editan en la
pantalla del tema (re-firma el índice, no toca el ZIP).

## Comandos útiles

| Comando | Para qué |
|---|---|
| `python -m adestock_temas publicar t.zip --miniatura m.webp --captura v1.webp --etiquetas a,b` | Misma validación/publicación que el panel, por consola |
| `python -m adestock_temas verificar [--clave <b64>]` | Recalcula sha256/bytes, re-valida ZIP y comprueba la firma |
| `python -m adestock_temas republicar-indice` | Regenera y vuelve a firmar el índice (p. ej. tras rotar clave) |
| `python -m adestock_temas backup [--destino D:\backups]` | ZIP con `api/temas-revista/`, `catalogo.json` y auditoría |
| `python -m adestock_temas clave-publica [--pem]` | Muestra la clave pública |
| `python -m adestock_temas cambiar-password` / `nuevo-2fa` | Cambio de contraseña (re-cifra la clave) / nuevo secreto TOTP |

## Reglas que aplica el validador (resumen)

ZIP ≤ 8 MB, ≤ 20 entradas, ≤ 16 MB descomprimido, sin cifrar, sin enlaces simbólicos, sin duplicados, nombres solo
`[A-Za-z0-9._-]`, sin `..` `\` `:`, sin datos extra antes/después; solo `tema.json`, `tema.css`, `fondo.*`,
`vista-previa.webp`, `INSTRUCCIONES-PARA-IA.md` (cualquier otro archivo se **rechaza**, más estricto que el README, que
solo lo ignora). `tema.json` con listas cerradas (colores `#rrggbb`, 5 fuentes, rangos, claves desconocidas rechazadas).
`tema.css` con lista blanca de selectores y propiedades; se rechazan `url()`, `@…`, `!important`, `expression`, `javascript:`,
escapes `\`, `position: fixed`, `absolute` fuera de `::before/::after`, `z-index > 5`. SVG sin `<script>`, `foreignObject`,
animaciones, eventos `on*`, DOCTYPE/ENTITY ni href externos. Imágenes: firma real + Pillow (formato, píxeles).

Interpretaciones del README (tema.css): se permiten además `font-size` (el README manda usar `cqw` para letras),
`position: relative|static`, y `top/right/bottom/left/inset` + `content` **solo** en `::before/::after`.

## Firma del índice y rotación de clave

`index.json.sig` = Ed25519 sobre los bytes exactos de `index.json`, en base64 (una línea). La clave pública se incrusta
en el Adestock, que verifica la firma **y** el sha256 de cada ZIP. Verificación de referencia (Python):

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
import base64
Ed25519PublicKey.from_public_bytes(base64.b64decode(PUBLICA_B64)).verify(base64.b64decode(sig_b64), indice_bytes)  # lanza InvalidSignature
```

**Rotar la clave sin cortar el servicio:**

1. `python -m adestock_temas rotar-clave` (pide la contraseña): archiva la clave vieja en `claves-anteriores/`, crea la nueva
   y re-firma el índice. **No hagas push todavía.**
2. Publicá una versión del Adestock que confíe en **ambas** claves (lista de claves permitidas; acepta la firma si alguna valida).
3. Esperá a que los clientes actualicen; recién entonces hacé push del índice firmado con la clave nueva.
4. En una versión posterior, quitá la clave vieja del Adestock.

Si se filtra la clave privada: rotá de inmediato (pasos 1–3 sin esperar) y sacá la clave vieja en cuanto sea posible. La clave
privada está cifrada con tu contraseña y nunca sale del directorio de estado.

## Seguridad del panel

Solo `127.0.0.1`; verificación de `Host` (anti DNS-rebinding) y `Origin`; contraseña con scrypt + TOTP (no reutilizable);
5 fallos en 15 min bloquean el login 15 min; sesión de 30 min de inactividad / 8 h máximo, rotada al entrar y revocable;
cookie `HttpOnly` + `SameSite=Strict`; CSRF en todo POST; CSP estricta (sin scripts); re-pedido de contraseña para
publicar/editar/retirar (también descifra la clave de firma); auditoría en JSON encadenado por hash (quién, cuándo, archivo,
sha256; detecta ediciones o borrados); cada publicación revierte todo si falla a mitad y toma un snapshot previo.

## Pruebas

```powershell
cd tools/admin-temas; python -m pytest tests -q
```

Cubren: tema válido, CSS prohibido (30 casos), ZIP con `..`/`\`/`:`/absoluta/symlink/cifrado/duplicados/exceso de entradas,
ZIP bomba (por tamaño y por ratio), tamaño declarado falso, SVG con script/foreignObject/href externo, sha256 que no
coincide, firma inválida, inmutabilidad de versiones, ids no reutilizables, retiro, rollback, backup, auditoría, rotación de
clave y toda la capa web (subida sin sesión, login, bloqueo, TOTP, CSRF, host, expiración de sesión, flujo completo).

## Hosting (importante)

`_headers` (HSTS, `Content-Type`, `Cache-Control`, `Content-Disposition: attachment` en los ZIP, `nosniff`) lo respetan
**Cloudflare Pages / Netlify**. **GitHub Pages lo ignora**: allí no se puede fijar `Content-Disposition` ni cachés
propias (el `<a download>` de la página compensa en parte). Si hoy se sirve desde GitHub Pages, poner Cloudflare delante
resuelve todo. Los uploads son archivos estáticos; nada se interpreta como HTML.
