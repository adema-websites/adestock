"""Validación de ZIP de tema y de imágenes de la tienda (README secciones 2, 3 y 3.4).

Nada se confía: se valida la estructura ANTES de leer, y cada lectura tiene tope propio.
Todo en memoria; nunca se extrae a disco.
"""
import io
import json
import re
import stat
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field

from . import config as C
from .css_validador import validar_css

FORMATOS = ("a4", "a4h", "post", "postv", "historia")
BASES = ("super", "oscuro", "minimal", "verano")
COLORES = ("fondo", "cabecera_fondo", "cabecera_texto", "titulo", "tarjeta", "texto", "texto_suave",
           "precio", "promo", "sello_fondo", "sello_texto", "franja_fondo", "franja_texto",
           "vigencia_fondo", "vigencia_texto", "pie_fondo", "pie_texto")
FUENTES = ("archivo", "barlow-cond", "barlow", "baloo", "fraunces")
FORMAS_SELLO = ("circulo", "cuadrado", "pastilla")
PRODUCTO = "adestock-revista-tema"

RE_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RE_VERSION = re.compile(r"^(0|[1-9]\d{0,5})\.(0|[1-9]\d{0,5})\.(0|[1-9]\d{0,5})$")
RE_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")
RE_SEGMENTO = re.compile(r"^[A-Za-z0-9._-]+$")
RE_ETIQUETA = re.compile(r"^[a-z0-9áéíóúñ]+(-[a-z0-9áéíóúñ]+)*$")

ARCHIVOS_FIJOS = {
    "tema.json": C.JSON_MAX_BYTES,
    "tema.css": C.CSS_MAX_BYTES,
    "vista-previa.webp": C.VISTA_PREVIA_MAX_BYTES,
    "INSTRUCCIONES-PARA-IA.md": C.INSTRUCCIONES_MAX_BYTES,
}
EXT_FONDO = (".webp", ".png", ".jpg", ".jpeg", ".svg")


@dataclass
class Resultado:
    errores: list = field(default_factory=list)
    avisos: list = field(default_factory=list)
    tema: dict = field(default_factory=dict)
    sha256: str = ""
    bytes: int = 0

    @property
    def ok(self) -> bool:
        return not self.errores


# ---------------------------------------------------------------- imágenes

def _firma_imagen(data: bytes, ext: str):
    if ext == ".webp":
        return data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    if ext == ".png":
        return data[:8] == b"\x89PNG\r\n\x1a\n"
    if ext in (".jpg", ".jpeg"):
        return data[:3] == b"\xff\xd8\xff"
    return False


def validar_imagen_raster(data: bytes, ext: str, nombre: str, errores: list):
    """Firma + (si Pillow está) formato real, dimensiones y tope de píxeles (anti bomba de descompresión)."""
    if not _firma_imagen(data, ext):
        errores.append(f"{nombre}: el contenido no es una imagen {ext[1:].upper()} real.")
        return None
    try:
        from PIL import Image
    except ImportError:  # pragma: no cover
        return None
    try:
        Image.MAX_IMAGE_PIXELS = C.IMAGEN_MAX_PIXELES
        with Image.open(io.BytesIO(data)) as im:
            fmt = (im.format or "").lower()
            esperado = {".webp": "webp", ".png": "png", ".jpg": "jpeg", ".jpeg": "jpeg"}[ext]
            if fmt != esperado:
                errores.append(f"{nombre}: la extensión {ext} no coincide con el formato real ({fmt}).")
                return None
            w, h = im.size
            if w * h > C.IMAGEN_MAX_PIXELES:
                errores.append(f"{nombre}: demasiados píxeles ({w}×{h}).")
                return None
            im.verify()
            return (w, h)
    except Exception as exc:  # noqa: BLE001 - cualquier fallo de decodificación = rechazo
        errores.append(f"{nombre}: imagen corrupta o no válida ({type(exc).__name__}).")
        return None


_SVG_PROHIBIDOS = {"script", "foreignobject", "iframe", "embed", "object", "audio", "video", "canvas",
                   "animate", "set", "animatemotion", "animatetransform", "handler", "listener"}
_RE_URL_EXTERNA = re.compile(r"url\s*\(\s*['\"]?\s*(?!#)", re.I)


def validar_svg(data: bytes, nombre: str, errores: list):
    try:
        texto = data.decode("utf-8")
    except UnicodeDecodeError:
        errores.append(f"{nombre}: el SVG no es UTF-8.")
        return
    bajo = texto.lower()
    if "<!doctype" in bajo or "<!entity" in bajo:
        errores.append(f"{nombre}: el SVG no puede tener DOCTYPE/ENTITY.")
        return
    if "<?xml-stylesheet" in bajo:
        errores.append(f"{nombre}: el SVG no puede enlazar hojas de estilo.")
        return
    try:
        raiz = ET.fromstring(texto)
    except ET.ParseError as exc:
        errores.append(f"{nombre}: SVG mal formado ({exc}).")
        return
    if raiz.tag.rsplit("}", 1)[-1].lower() != "svg":
        errores.append(f"{nombre}: la raíz no es <svg>.")
        return
    n = 0
    for el in raiz.iter():
        n += 1
        if n > 20000:
            errores.append(f"{nombre}: SVG demasiado complejo.")
            return
        tag = el.tag.rsplit("}", 1)[-1].lower() if isinstance(el.tag, str) else ""
        if tag in _SVG_PROHIBIDOS:
            errores.append(f"{nombre}: el SVG contiene <{tag}>, que no está permitido.")
            return
        if tag == "style" and (_RE_URL_EXTERNA.search(el.text or "") or "@import" in (el.text or "").lower()):
            errores.append(f"{nombre}: <style> del SVG con recursos externos.")
            return
        for attr, val in el.attrib.items():
            a = attr.rsplit("}", 1)[-1].lower()
            v = val.strip()
            if a.startswith("on"):
                errores.append(f"{nombre}: atributo de evento «{a}» no permitido en SVG.")
                return
            if a == "href" and not v.startswith("#"):
                errores.append(f"{nombre}: href externo en SVG («{v[:40]}»).")
                return
            if "javascript:" in v.lower() or _RE_URL_EXTERNA.search(v) or "@import" in v.lower():
                errores.append(f"{nombre}: atributo «{a}» del SVG referencia recursos externos o scripts.")
                return


# ---------------------------------------------------------------- tema.json

def _rechazar_duplicados(pares):
    d = {}
    for k, v in pares:
        if k in d:
            raise ValueError(f"clave duplicada «{k}»")
        d[k] = v
    return d


def _texto(valor, nombre, maximo, errores, obligatorio=True):
    if not isinstance(valor, str):
        if obligatorio:
            errores.append(f"tema.json: «{nombre}» debe ser texto.")
        return
    if obligatorio and not valor.strip():
        errores.append(f"tema.json: «{nombre}» no puede estar vacío.")
    if len(valor) > maximo:
        errores.append(f"tema.json: «{nombre}» supera {maximo} caracteres.")
    if re.search(r"[\x00-\x1f\x7f<>]", valor):
        errores.append(f"tema.json: «{nombre}» contiene caracteres no permitidos (< > o de control).")


def validar_tema_json(data: bytes, errores: list):
    try:
        obj = json.loads(data.decode("utf-8-sig"), object_pairs_hook=_rechazar_duplicados,
                         parse_constant=lambda c: (_ for _ in ()).throw(ValueError(c)))
    except (UnicodeDecodeError, ValueError, RecursionError) as exc:
        errores.append(f"tema.json no es un JSON válido ({exc}).")
        return None
    if not isinstance(obj, dict):
        errores.append("tema.json debe ser un objeto JSON.")
        return None
    permitidas = {"formato", "producto", "id", "nombre", "descripcion", "autor", "version", "base",
                  "valores", "fondo"}
    for k in obj:
        if k not in permitidas:
            errores.append(f"tema.json: campo no permitido «{k}».")
    if obj.get("formato") != C.FORMATO_ACTUAL or isinstance(obj.get("formato"), bool):
        errores.append(f"tema.json: «formato» debe ser {C.FORMATO_ACTUAL}.")
    if obj.get("producto") != PRODUCTO:
        errores.append(f"tema.json: «producto» debe ser «{PRODUCTO}».")
    tid = obj.get("id")
    if not isinstance(tid, str) or not RE_ID.match(tid) or len(tid) > 50:
        errores.append("tema.json: «id» inválido (minúsculas, números y guiones; máx. 50).")
    ver = obj.get("version")
    if not isinstance(ver, str) or not RE_VERSION.match(ver):
        errores.append("tema.json: «version» debe ser MAYOR.MENOR.PARCHE (p. ej. 1.0.0).")
    _texto(obj.get("nombre"), "nombre", 60, errores)
    _texto(obj.get("descripcion"), "descripcion", 300, errores)
    _texto(obj.get("autor"), "autor", 60, errores)
    if obj.get("base") not in BASES:
        errores.append(f"tema.json: «base» debe ser una de {', '.join(BASES)}.")

    valores = obj.get("valores")
    if not isinstance(valores, dict):
        errores.append("tema.json: falta «valores» (objeto).")
        valores = {}
    ok_val = {"colores", "fuente_titulo", "fuente_texto", "fuente_precio", "radio_tarjeta",
              "forma_sello", "sello_inclinado", "sombra", "fondo_velo"}
    for k in valores:
        if k not in ok_val:
            errores.append(f"tema.json: valor no permitido «valores.{k}».")
    colores = valores.get("colores", {})
    if not isinstance(colores, dict):
        errores.append("tema.json: «valores.colores» debe ser un objeto.")
        colores = {}
    for k, v in colores.items():
        if k not in COLORES:
            errores.append(f"tema.json: color desconocido «{k}».")
        elif not isinstance(v, str) or not RE_COLOR.match(v):
            errores.append(f"tema.json: el color «{k}» debe ser #rrggbb (6 dígitos).")
    for f in ("fuente_titulo", "fuente_texto", "fuente_precio"):
        if f in valores and valores[f] not in FUENTES:
            errores.append(f"tema.json: «{f}» debe ser una de {', '.join(FUENTES)}.")
    if "radio_tarjeta" in valores:
        r = valores["radio_tarjeta"]
        if isinstance(r, bool) or not isinstance(r, int) or not 0 <= r <= 30:
            errores.append("tema.json: «radio_tarjeta» debe ser un entero de 0 a 30.")
    if "forma_sello" in valores and valores["forma_sello"] not in FORMAS_SELLO:
        errores.append(f"tema.json: «forma_sello» debe ser una de {', '.join(FORMAS_SELLO)}.")
    for b in ("sello_inclinado", "sombra"):
        if b in valores and not isinstance(valores[b], bool):
            errores.append(f"tema.json: «{b}» debe ser true o false.")
    if "fondo_velo" in valores:
        r = valores["fondo_velo"]
        if isinstance(r, bool) or not isinstance(r, int) or not 0 <= r <= 80:
            errores.append("tema.json: «fondo_velo» debe ser un entero de 0 a 80.")
    fondo = obj.get("fondo")
    if fondo is not None:
        if not isinstance(fondo, dict) or set(fondo) != {"archivo"} or not isinstance(fondo["archivo"], str):
            errores.append("tema.json: «fondo» debe ser {\"archivo\": \"fondo.ext\"}.")
        elif not re.fullmatch(r"fondo\.(webp|png|jpg|jpeg|svg)", fondo["archivo"]):
            errores.append("tema.json: «fondo.archivo» debe llamarse fondo.webp|png|jpg|jpeg|svg.")
    return obj


# ---------------------------------------------------------------- ZIP

def _estructura(zf: zipfile.ZipFile, data: bytes, res: Resultado):
    """Devuelve {nombre_normalizado: ZipInfo} o None. No lee contenido."""
    e = res.errores
    infos = zf.infolist()
    if zf.comment:
        e.append("El ZIP no puede tener comentario.")
    if data[:4] != b"PK\x03\x04" or data[-22:-18] != b"PK\x05\x06":
        e.append("El ZIP tiene datos antes/después de su estructura (formato no estándar).")
    if len(infos) > C.ZIP_MAX_ARCHIVOS:
        e.append(f"El ZIP tiene {len(infos)} entradas (máximo {C.ZIP_MAX_ARCHIVOS}).")
        return None
    vistos, total = set(), 0
    por_nombre = {}
    for zi in infos:
        n = zi.filename
        if zi.flag_bits & 0x1:
            e.append(f"«{n}»: el ZIP está cifrado (con contraseña); no se admite.")
            return None
        if zi.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
            e.append(f"«{n}»: método de compresión no admitido.")
            return None
        if "\\" in n or ":" in n or "\x00" in n or n.startswith("/") or n.startswith("~"):
            e.append(f"Ruta peligrosa en el ZIP: «{n}» (no se permiten «\\», «:» ni rutas absolutas).")
            return None
        trozos = n.rstrip("/").split("/")
        if any(t in ("..", ".", "") or not RE_SEGMENTO.match(t) for t in trozos):
            e.append(f"Ruta no permitida en el ZIP: «{n}».")
            return None
        modo = (zi.external_attr >> 16) & 0xFFFF
        tipo = stat.S_IFMT(modo)
        if tipo == stat.S_IFLNK:
            e.append(f"«{n}» es un enlace simbólico; no se admite.")
            return None
        if tipo and tipo not in (stat.S_IFREG, stat.S_IFDIR):
            e.append(f"«{n}» no es un archivo regular.")
            return None
        clave = n.rstrip("/").casefold()
        if clave in vistos:
            e.append(f"Entrada duplicada en el ZIP: «{n}».")
            return None
        vistos.add(clave)
        if zi.is_dir():
            continue
        total += zi.file_size
        if zi.compress_size and zi.file_size > 1_000_000 and zi.file_size / zi.compress_size > C.RATIO_SOSPECHOSO:
            e.append(f"«{n}»: relación de compresión sospechosa (posible ZIP bomba).")
            return None
        por_nombre[n] = zi
    if total > C.ZIP_MAX_DESCOMPRIMIDO:
        e.append(f"El contenido descomprimido ({total} bytes) supera el tope de {C.ZIP_MAX_DESCOMPRIMIDO} (posible ZIP bomba).")
        return None
    return por_nombre


def _normalizar_raiz(por_nombre: dict, e: list):
    if "tema.json" in por_nombre:
        return por_nombre
    carpetas = {n.split("/", 1)[0] for n in por_nombre if "/" in n}
    if len(carpetas) == 1 and all(n.startswith(next(iter(carpetas)) + "/") for n in por_nombre):
        pref = next(iter(carpetas)) + "/"
        nuevo = {n[len(pref):]: zi for n, zi in por_nombre.items()}
        if "tema.json" in nuevo:
            return nuevo
    e.append("Falta tema.json en la raíz del ZIP (o dentro de una única carpeta).")
    return None


def _leer(zf, zi, limite, e):
    try:
        with zf.open(zi) as fh:
            datos = fh.read(limite + 1)
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, OSError, EOFError) as exc:
        e.append(f"«{zi.filename}»: no se pudo leer ({exc}).")
        return None
    if len(datos) > limite:
        e.append(f"«{zi.filename}» supera el límite de {limite} bytes.")
        return None
    if len(datos) != zi.file_size:
        e.append(f"«{zi.filename}»: el tamaño declarado no coincide con el real (ZIP manipulado).")
        return None
    return datos


def validar_zip(data: bytes) -> Resultado:
    import hashlib
    res = Resultado(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    e = res.errores
    if len(data) > C.ZIP_MAX_BYTES:
        e.append(f"El ZIP pesa {len(data)} bytes (máximo {C.ZIP_MAX_BYTES}).")
        return res
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except (zipfile.BadZipFile, ValueError, OSError) as exc:
        e.append(f"No es un ZIP válido ({exc}).")
        return res
    with zf:
        por_nombre = _estructura(zf, data, res)
        if por_nombre is None:
            return res
        por_nombre = _normalizar_raiz(por_nombre, e)
        if por_nombre is None:
            return res
        fondo_nombre = None
        for n in por_nombre:
            if n in ARCHIVOS_FIJOS:
                continue
            if re.fullmatch(r"fondo\.(webp|png|jpg|jpeg|svg)", n):
                if fondo_nombre:
                    e.append("Hay más de un archivo fondo.* en el ZIP.")
                fondo_nombre = n
                continue
            e.append(f"Archivo no permitido en el ZIP: «{n}» (solo tema.json, tema.css, fondo.*, "
                     "vista-previa.webp, INSTRUCCIONES-PARA-IA.md).")
        if e:
            return res
        tema = validar_tema_json(_leer(zf, por_nombre["tema.json"], C.JSON_MAX_BYTES, e) or b"", e) \
            if "tema.json" in por_nombre else None
        res.tema = tema or {}
        if "tema.css" in por_nombre:
            css = _leer(zf, por_nombre["tema.css"], C.CSS_MAX_BYTES, e)
            if css is not None:
                e.extend(f"tema.css: {m}" for m in validar_css(css))
        declarado = (tema or {}).get("fondo", {}).get("archivo") if isinstance((tema or {}).get("fondo"), dict) else None
        if declarado and declarado != fondo_nombre:
            e.append(f"tema.json declara «{declarado}» pero el ZIP no lo contiene.")
        if fondo_nombre and not declarado:
            e.append(f"El ZIP trae «{fondo_nombre}» pero tema.json no lo declara en «fondo».")
        if fondo_nombre:
            datos = _leer(zf, por_nombre[fondo_nombre], C.FONDO_MAX_BYTES, e)
            if datos is not None:
                ext = "." + fondo_nombre.rsplit(".", 1)[1]
                if ext == ".svg":
                    validar_svg(datos, fondo_nombre, e)
                else:
                    validar_imagen_raster(datos, ext, fondo_nombre, e)
        if "vista-previa.webp" in por_nombre:
            datos = _leer(zf, por_nombre["vista-previa.webp"], C.VISTA_PREVIA_MAX_BYTES, e)
            if datos is not None:
                validar_imagen_raster(datos, ".webp", "vista-previa.webp", e)
        if "INSTRUCCIONES-PARA-IA.md" in por_nombre:
            datos = _leer(zf, por_nombre["INSTRUCCIONES-PARA-IA.md"], C.INSTRUCCIONES_MAX_BYTES, e)
            if datos is not None:
                try:
                    datos.decode("utf-8")
                except UnicodeDecodeError:
                    e.append("INSTRUCCIONES-PARA-IA.md no es UTF-8.")
    return res


def validar_imagen_tienda(data: bytes, nombre: str, maximo: int, errores: list):
    """Miniatura y capturas de la galería: WebP, con tope de peso."""
    if len(data) > maximo:
        errores.append(f"{nombre} pesa {len(data)} bytes (máximo {maximo}).")
        return
    dims = validar_imagen_raster(data, ".webp", nombre, errores)
    if dims and (dims[0] > 2400 or dims[1] > 2400):
        errores.append(f"{nombre}: dimensiones excesivas ({dims[0]}×{dims[1]}).")


def validar_etiquetas(etiquetas, errores: list):
    if len(etiquetas) > 8:
        errores.append("Máximo 8 etiquetas.")
    for t in etiquetas:
        if not isinstance(t, str) or len(t) > 24 or not RE_ETIQUETA.match(t):
            errores.append(f"Etiqueta inválida «{t}» (minúsculas, números y guiones; máx. 24).")


def validar_formatos(formatos, errores: list):
    if not formatos:
        errores.append("Elegí al menos un formato.")
    for f in formatos:
        if f not in FORMATOS:
            errores.append(f"Formato desconocido «{f}».")
