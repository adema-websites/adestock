"""Validador de tema.css (README sección 3.2): lista blanca de selectores y propiedades.

Estrategia: no se "limpia" el CSS, se RECHAZA todo lo que no esté explícitamente permitido.
"""
import re

from .config import CSS_MAX_BYTES

SELECTORES_CLASE = frozenset({
    "hoja", "h-cab", "h-marca", "h-logo", "h-titulos", "h-titulo", "h-vig", "h-cuerpo", "h-pie",
    "ribbon", "seccion", "grilla", "card", "foto", "sello", "info", "nombre", "pres",
    "precio-zona", "antes", "precio", "etq-precio", "leyenda-promo", "extra", "dia", "hero",
    "hero-card", "hero-info", "portada", "portada-titulo", "portada-sub",
})

_LADOS = ("top", "right", "bottom", "left")
PROPIEDADES = {
    "color", "background", "background-color", "background-image", "background-size",
    "background-position", "background-repeat",
    "border", "border-width", "border-style", "border-color", "border-radius",
    "outline", "outline-color", "outline-style", "outline-width", "outline-offset",
    "box-shadow", "text-shadow", "filter",
    "font-weight", "font-style", "font-size", "letter-spacing", "text-transform",
    "line-height", "text-align",
    "padding", "margin", "gap", "row-gap", "column-gap",
    "width", "height", "min-width", "min-height", "max-width", "max-height", "aspect-ratio",
    "transform", "opacity", "content", "position", "z-index",
    "top", "right", "bottom", "left", "inset",
}
for _l in _LADOS:
    PROPIEDADES |= {f"border-{_l}", f"border-{_l}-width", f"border-{_l}-style", f"border-{_l}-color",
                    f"padding-{_l}", f"margin-{_l}"}
for _v in ("top", "bottom"):
    for _h in ("left", "right"):
        PROPIEDADES.add(f"border-{_v}-{_h}-radius")

SOLO_PSEUDO = {"content", "top", "right", "bottom", "left", "inset"}

FUNCIONES = {
    "linear-gradient", "radial-gradient", "repeating-linear-gradient", "calc", "var",
    "rgba", "rgb", "hsl", "hsla", "rotate", "scale", "translate", "translatex", "translatey",
    "scalex", "scaley", "drop-shadow",
}
GRADIENTES = {"linear-gradient", "radial-gradient", "repeating-linear-gradient"}
PROHIBIDAS_PALABRA = ("expression", "javascript", "behavior", "binding", "vbscript", "@import")

MAX_REGLAS = 400
MAX_SELECTORES_POR_REGLA = 20
MAX_CONTENT = 30

_RE_FUNC = re.compile(r"([a-zA-Z_][\w-]*)\s*\(")
_RE_CLASE = re.compile(r"\.([a-zA-Z_][\w-]*)")
_RE_NTH = re.compile(r"^:nth-child\((odd|even|[+-]?\d*n?(?:[+-]\d+)?)\)")
_RE_VAR = re.compile(r"var\(\s*(--[\w-]*)")


def _quitar_comentarios(css: str, errores: list) -> str:
    out, i, n = [], 0, len(css)
    while i < n:
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            if j < 0:
                errores.append("Comentario CSS sin cerrar.")
                return ""
            out.append(" ")
            i = j + 2
        else:
            out.append(css[i])
            i += 1
    return "".join(out)


def _bloques(css: str, errores: list):
    """Devuelve [(selector, cuerpo)] y verifica llaves planas, balanceadas y comillas cerradas."""
    reglas, i, n = [], 0, len(css)
    sel_ini = 0
    while i < n:
        c = css[i]
        if c in "\"'":
            j = css.find(c, i + 1)
            if j < 0 or "\n" in css[i:j]:
                errores.append("Comillas sin cerrar en el CSS.")
                return reglas
            i = j + 1
            continue
        if c == "}":
            errores.append("Llave de cierre '}' sin apertura.")
            return reglas
        if c == "{":
            selector = css[sel_ini:i].strip()
            j, k = i + 1, i + 1
            while k < n:
                ck = css[k]
                if ck in "\"'":
                    e = css.find(ck, k + 1)
                    if e < 0:
                        errores.append("Comillas sin cerrar en el CSS.")
                        return reglas
                    k = e + 1
                    continue
                if ck == "{":
                    errores.append("Reglas anidadas no permitidas.")
                    return reglas
                if ck == "}":
                    break
                k += 1
            else:
                errores.append("Llave '{' sin cerrar.")
                return reglas
            reglas.append((selector, css[j:k]))
            i = k + 1
            sel_ini = i
            continue
        i += 1
    if css[sel_ini:].strip():
        errores.append("Texto suelto fuera de una regla (¿falta una llave?).")
    return reglas


def _validar_selector(sel: str, errores: list) -> str:
    """Valida un selector simple. Devuelve 'pseudo' si termina en ::before/::after, '' si no, None si inválido."""
    s = re.sub(r"\(([^)]*)\)", lambda m: "(" + re.sub(r"\s+", "", m.group(1)) + ")", sel.strip())
    s = re.sub(r"\s*>\s*", " > ", s)
    tokens = s.split()
    if not tokens:
        errores.append("Selector vacío.")
        return None
    esperado_comp = True
    pseudo = ""
    for idx, tok in enumerate(tokens):
        if tok == ">":
            if esperado_comp:
                errores.append(f"Selector no permitido: «{sel.strip()}».")
                return None
            esperado_comp = True
            continue
        if not esperado_comp:
            esperado_comp = True  # descendiente (espacio)
        ultimo = idx == len(tokens) - 1
        resto, clases = tok, 0
        while resto:
            m = _RE_CLASE.match(resto)
            if m:
                if m.group(1) not in SELECTORES_CLASE:
                    errores.append(f"Clase fuera de la lista blanca: «.{m.group(1)}».")
                    return None
                clases += 1
                resto = resto[m.end():]
                continue
            if resto.startswith("::before") or resto.startswith("::after"):
                largo = 8 if resto.startswith("::before") else 7
                if not ultimo or resto[largo:]:
                    errores.append("::before/::after solo puede ir al final del selector.")
                    return None
                pseudo = "pseudo"
                resto = ""
                continue
            if resto.startswith(":first-child") or resto.startswith(":last-child"):
                resto = resto[12:] if resto.startswith(":first-child") else resto[11:]
                continue
            m = _RE_NTH.match(resto)
            if m and m.group(1):
                resto = resto[m.end():]
                continue
            errores.append(f"Selector no permitido: «{sel.strip()}» (solo clases de la hoja, sin ids, "
                           "etiquetas, atributos ni «*»).")
            return None
        if clases == 0:
            errores.append(f"Selector sin clase de la hoja: «{sel.strip()}».")
            return None
        esperado_comp = False
    if esperado_comp:
        errores.append(f"Selector incompleto: «{sel.strip()}».")
        return None
    return pseudo


def _dividir_declaraciones(cuerpo: str):
    decls, actual, prof, i = [], [], 0, 0
    while i < len(cuerpo):
        c = cuerpo[i]
        if c in "\"'":
            j = cuerpo.find(c, i + 1)
            actual.append(cuerpo[i:j + 1])
            i = j + 1
            continue
        if c == "(":
            prof += 1
        elif c == ")":
            prof -= 1
        if c == ";" and prof == 0:
            decls.append("".join(actual))
            actual = []
        else:
            actual.append(c)
        i += 1
    if "".join(actual).strip():
        decls.append("".join(actual))
    return decls


def _funciones(valor: str):
    return [m.group(1).lower() for m in _RE_FUNC.finditer(valor)]


def _top_level(valor: str, sep: str):
    partes, prof, actual = [], 0, []
    for c in valor:
        if c == "(":
            prof += 1
        elif c == ")":
            prof -= 1
        if c == sep and prof == 0:
            partes.append("".join(actual).strip())
            actual = []
        else:
            actual.append(c)
    partes.append("".join(actual).strip())
    return partes


def _validar_valor(prop: str, valor: str, todos_pseudo: bool, errores: list):
    v = valor.strip()
    low = re.sub(r"\s+", "", v.lower())
    if not v:
        errores.append(f"«{prop}» sin valor.")
        return
    if "!important" in low or "!" in v:
        errores.append(f"«!important» (o «!») no está permitido (propiedad «{prop}»).")
        return
    if re.search(r"url\s*\(", v, re.I) or "url(" in low:
        errores.append(f"«url()» no está permitido (propiedad «{prop}»). Las imágenes viajan como fondo.*.")
        return
    for pal in PROHIBIDAS_PALABRA:
        if pal in low:
            errores.append(f"Valor prohibido «{pal}» en la propiedad «{prop}».")
            return
    for f in _funciones(v):
        if f not in FUNCIONES:
            errores.append(f"Función CSS no permitida: «{f}()» (propiedad «{prop}»).")
            return
    for nombre in _RE_VAR.findall(v):
        if not nombre.startswith("--t-"):
            errores.append(f"var() solo puede usar variables --t-* (encontrado «{nombre}»).")
            return
    if prop == "position":
        if low in ("fixed", "sticky"):
            errores.append(f"«position: {low}» no está permitido.")
        elif low == "absolute":
            if not todos_pseudo:
                errores.append("«position: absolute» solo se permite en ::before/::after.")
        elif low not in ("relative", "static"):
            errores.append(f"Valor de position no permitido: «{v}».")
    elif prop == "z-index":
        if not re.fullmatch(r"-?\d+", low) or not -5 <= int(low) <= 5:
            errores.append("z-index debe ser un entero entre -5 y 5.")
    elif prop == "content":
        if low not in ("none", "normal", '""', "''") and not re.fullmatch(r'("[^"\\]*"|\'[^\'\\]*\')', v):
            errores.append("content solo admite texto entre comillas (corto), «none» o «normal».")
        elif v[:1] in "\"'" and len(v) - 2 > MAX_CONTENT:
            errores.append(f"content demasiado largo (máx. {MAX_CONTENT} caracteres).")
    elif prop == "filter":
        for item in (t for t in _top_level(v, " ") if t):
            if not item.lower().startswith("drop-shadow("):
                errores.append("filter solo admite drop-shadow().")
                break
    elif prop == "background-image":
        for item in _top_level(v, ","):
            fs = _funciones(item)
            if item.lower() != "none" and not (fs and fs[0] in GRADIENTES and item.lower().startswith(fs[0])):
                errores.append("background-image solo admite gradientes.")
                break


def validar_css(css_bytes: bytes):
    """Devuelve lista de errores (vacía = válido)."""
    errores: list = []
    if len(css_bytes) > CSS_MAX_BYTES:
        return [f"tema.css supera {CSS_MAX_BYTES} bytes ({len(css_bytes)})."]
    try:
        texto = css_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return ["tema.css no es UTF-8 válido."]
    if "\x00" in texto or re.search(r"[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]", texto):
        return ["tema.css contiene caracteres de control."]
    if "\\" in texto:
        return ["tema.css no puede contener «\\» (escapes CSS permiten ocultar url() u otras construcciones)."]
    if "<" in texto:
        return ["tema.css no puede contener «<»."]
    if "@" in texto:
        return ["At-rules no permitidas (@import, @font-face, @media, @keyframes, …): no se admite «@»."]
    texto = _quitar_comentarios(texto, errores)
    if errores:
        return errores
    reglas = _bloques(texto, errores)
    if errores:
        return errores
    if len(reglas) > MAX_REGLAS:
        return [f"Demasiadas reglas CSS (máx. {MAX_REGLAS})."]
    for selector, cuerpo in reglas:
        sels = _top_level(selector, ",")
        if len(sels) > MAX_SELECTORES_POR_REGLA:
            errores.append("Demasiados selectores en una regla.")
            continue
        tipos = [_validar_selector(s, errores) for s in sels]
        if any(t is None for t in tipos):
            continue
        todos_pseudo = all(t == "pseudo" for t in tipos)
        for decl in _dividir_declaraciones(cuerpo):
            if not decl.strip():
                continue
            if ":" not in decl:
                errores.append(f"Declaración inválida: «{decl.strip()[:40]}».")
                continue
            prop, valor = decl.split(":", 1)
            prop = prop.strip().lower()
            if prop.startswith("--t-") and re.fullmatch(r"--t-[a-z0-9-]+", prop):
                _validar_valor(prop, valor, todos_pseudo, errores)
                continue
            if prop not in PROPIEDADES:
                errores.append(f"Propiedad no permitida: «{prop}».")
                continue
            if prop in SOLO_PSEUDO and not todos_pseudo:
                errores.append(f"«{prop}» solo se permite en ::before/::after.")
                continue
            _validar_valor(prop, valor, todos_pseudo, errores)
    # sin duplicar mensajes
    vistos, unicos = set(), []
    for e in errores:
        if e not in vistos:
            vistos.add(e)
            unicos.append(e)
    return unicos
