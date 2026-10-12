import json
import zipfile

import pytest

from adestock_temas.css_validador import validar_css
from adestock_temas.validador import validar_zip, validar_svg
from conftest import CSS_OK, hacer_zip, tema_dict, webp, zip_tema


def errores(data):
    return validar_zip(data).errores


# ------------------------------------------------------------- tema válido
def test_tema_valido_del_readme():
    r = validar_zip(zip_tema(fondo=("fondo.webp", webp(300, 400))))
    assert r.ok, r.errores
    assert r.tema["id"] == "navidad-dorado"
    assert len(r.sha256) == 64


def test_tema_minimo_sin_css_ni_fondo():
    assert validar_zip(zip_tema(css=None)).ok


def test_tolera_una_unica_carpeta_contenedora():
    inner = zip_tema(css=None)
    import io
    z = zipfile.ZipFile(io.BytesIO(inner))
    datos = {"mi-tema/" + n: z.read(n) for n in z.namelist()}
    assert validar_zip(hacer_zip(datos)).ok


# ------------------------------------------------------------- CSS prohibido
CSS_MALOS = [
    (".card{background:url(x.png)}", "url"),
    (".card{background-image:URL( 'x.png' )}", "url"),
    ('.card{background:\\75rl(x.png)}', "\\"),
    ("@import 'x.css';.card{color:red}", "@"),
    ("@font-face{font-family:x}", "@"),
    ("@media print{.card{color:red}}", "@"),
    ("@keyframes a{from{color:red}}", "@"),
    (".card{color:red !important}", "important"),
    (".card{width:expression(alert(1))}", "expression"),
    (".card{background:javascript:alert(1)}", "javascript"),
    (".card{position:fixed}", "fixed"),
    (".card{position:absolute}", "absolute"),
    (".card::before{z-index:99}", "z-index"),
    ("body{color:red}", "Selector"),
    ("#x{color:red}", "Selector"),
    ("*{color:red}", "Selector"),
    (".card[href]{color:red}", "Selector"),
    (".otra-clase{color:red}", "lista blanca"),
    (".card + .card{color:red}", "Selector"),
    (".card{display:none}", "Propiedad no permitida"),
    (".card{filter:blur(4px)}", "filter"),
    (".card{behavior:url(x.htc)}", "Propiedad no permitida"),
    (".card{content:\"x\"}", "::before"),
    (".card{color:var(--otra)}", "--t-"),
    (".card{background-image:url(data:image/png;base64,AAAA)}", "url"),
    (".card{color:red}}", "}"),
    (".card{color:red", "cerrar"),
    (".card{.sello{color:red}}", "anidadas"),
    (".card::before .sello{color:red}", "::before"),
    (".card{color:red} <script>", "<"),
]


@pytest.mark.parametrize("css,fragmento", CSS_MALOS)
def test_css_prohibido_se_rechaza(css, fragmento):
    errs = validar_css(css.encode())
    assert errs, f"debía rechazarse: {css}"
    assert any(fragmento.lower() in e.lower() for e in errs), errs


def test_css_pasa_dentro_del_zip_y_se_informa_el_motivo():
    errs = errores(zip_tema(css=".card{background:url(http://evil/x.png)}"))
    assert any(e.startswith("tema.css:") and "url()" in e for e in errs)


def test_css_valido_con_gradientes_vars_y_pseudo():
    css = (".hoja .card:nth-child(2n+1)>.sello{background:radial-gradient(circle,var(--t-sello-bg),rgba(0,0,0,.2));"
           "transform:rotate(-8deg) scale(1.1);box-shadow:0 2px 4px rgba(0,0,0,.3)}"
           ".card::after{content:'★';position:absolute;top:2px;left:3px;z-index:3}"
           ".precio{filter:drop-shadow(0 1px 1px #000);font-size:4cqw;--t-precio:#fff}")
    assert validar_css(css.encode()) == []


def test_css_demasiado_grande():
    assert validar_css(b"/*" + b"a" * 60000 + b"*/")


# ------------------------------------------------------------- ZIP peligrosos
def test_zip_con_punto_punto():
    z = hacer_zip({"tema.json": json.dumps(tema_dict()).encode(), "../fuera.txt": b"x"})
    assert any("Ruta" in e for e in errores(z))


@pytest.mark.parametrize("nombre", ["a\\b.txt", "C:evil.txt", "/abs.txt", "sub/../x.txt", "a/./b", "x\x00y"])
def test_zip_rutas_peligrosas(nombre):
    z = hacer_zip({"tema.json": json.dumps(tema_dict()).encode(), nombre: b"x"})
    assert errores(z)


def test_zip_con_enlace_simbolico():
    def extra(zf):
        zi = zipfile.ZipInfo("fondo.png", (2026, 1, 1, 0, 0, 0))
        zi.external_attr = 0o120777 << 16
        zf.writestr(zi, b"/etc/passwd")
    z = hacer_zip({"tema.json": json.dumps(tema_dict()).encode()}, extra)
    assert any("simbólico" in e for e in errores(z))


def test_zip_cifrado():
    z = bytearray(zip_tema(css=None))
    # Marca la entrada como cifrada (bit 0 de flag_bits) en la cabecera local y en el directorio central.
    for firma, off in ((b"PK", 6), (b"PK", 8)):
        i = z.find(firma)
        while i >= 0:
            z[i + off] |= 0x01
            i = z.find(firma, i + 4)
    assert any("cifrado" in e for e in errores(bytes(z)))


def test_zip_con_duplicados():
    import warnings

    def extra(zf):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            zf.writestr("tema.json", b"{}")
    z = hacer_zip({"tema.json": json.dumps(tema_dict()).encode()}, extra)
    assert any("duplicada" in e for e in errores(z))


def test_zip_con_demasiados_archivos():
    archivos = {"tema.json": json.dumps(tema_dict()).encode()}
    archivos.update({f"x{i}.txt": b"a" for i in range(25)})
    assert any("entradas" in e for e in errores(hacer_zip(archivos)))


def test_zip_con_archivo_no_permitido():
    z = hacer_zip({"tema.json": json.dumps(tema_dict()).encode(), "malware.exe": b"MZ"})
    assert any("no permitido" in e for e in errores(z))


def test_zip_bomba_por_tamano_descomprimido():
    # ~30 MB de ceros comprimen a unos KB: el tope es sobre lo DESCOMPRIMIDO.
    z = hacer_zip({"tema.json": json.dumps(tema_dict()).encode(), "INSTRUCCIONES-PARA-IA.md": b"\0" * (30 * 1024 * 1024)})
    assert len(z) < 1_000_000
    assert any("ZIP bomba" in e for e in errores(z))


def test_zip_bomba_por_ratio_en_fondo():
    z = hacer_zip({"tema.json": json.dumps(tema_dict(fondo={"archivo": "fondo.svg"})).encode(),
                   "fondo.svg": b"<svg xmlns='http://www.w3.org/2000/svg'>" + b" " * (4 * 1024 * 1024) + b"</svg>"})
    assert any("bomba" in e.lower() for e in errores(z))


def test_zip_mayor_a_8mb():
    import os
    z = hacer_zip({"tema.json": json.dumps(tema_dict()).encode(), "fondo.png": os.urandom(9 * 1024 * 1024)})
    assert any("máximo" in e for e in errores(z))


def test_zip_tamano_declarado_mentiroso():
    z = bytearray(zip_tema(css=None))
    # Falsifica el tamaño descomprimido en el directorio central (el que usa zipfile).
    import struct
    i = z.find(b"PK")
    real = struct.unpack("<I", z[i + 24:i + 28])[0]
    z[i + 24:i + 28] = struct.pack("<I", real + 5)
    assert errores(bytes(z))


def test_no_es_zip():
    assert any("ZIP" in e for e in errores(b"esto no es un zip"))


def test_zip_con_basura_al_final():
    assert errores(zip_tema(css=None) + b"EXTRA")


# ------------------------------------------------------------- SVG
SVG = "<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' width='10' height='10'>{}</svg>"


@pytest.mark.parametrize("cuerpo,fragmento", [
    ("<script>alert(1)</script>", "script"),
    ("<foreignObject><div>x</div></foreignObject>", "foreignobject"),
    ("<image href='http://evil/x.png'/>", "href externo"),
    ("<image xlink:href='https://evil/x.png'/>", "href externo"),
    ("<a href='javascript:alert(1)'><rect/></a>", "href externo"),
    ("<rect onload='alert(1)'/>", "evento"),
    ("<rect style='fill:url(http://evil/x)'/>", "externos"),
    ("<style>@import 'http://evil/x.css';</style>", "externos"),
    ("<animate attributeName='href' to='javascript:x'/>", "animate"),
])
def test_svg_peligroso(cuerpo, fragmento):
    errs = []
    validar_svg(SVG.format(cuerpo).encode(), "fondo.svg", errs)
    assert errs and fragmento in errs[0].lower(), errs


def test_svg_con_doctype_entity():
    errs = []
    validar_svg(b"<?xml version='1.0'?><!DOCTYPE svg [<!ENTITY x 'a'>]><svg xmlns='http://www.w3.org/2000/svg'/>", "f.svg", errs)
    assert errs


def test_svg_simple_ok():
    errs = []
    validar_svg(SVG.format("<defs><linearGradient id='g'/></defs><rect fill='url(#g)'/><use href='#g'/>").encode(), "f.svg", errs)
    assert errs == []


def test_svg_con_script_dentro_del_zip():
    svg = SVG.format("<script>alert(1)</script>").encode()
    errs = errores(zip_tema(css=None, fondo=("fondo.svg", svg)))
    assert any("script" in e.lower() for e in errs)


# ------------------------------------------------------------- tema.json
@pytest.mark.parametrize("cambio,fragmento", [
    ({"id": "Navidad_Dorado"}, "id"),
    ({"id": "-x"}, "id"),
    ({"version": "1.0"}, "version"),
    ({"version": "01.0.0"}, "version"),
    ({"base": "otra"}, "base"),
    ({"formato": 2}, "formato"),
    ({"producto": "otro"}, "producto"),
    ({"extra": 1}, "no permitido"),
    ({"nombre": "<b>x</b>"}, "nombre"),
])
def test_tema_json_invalido(cambio, fragmento):
    t = tema_dict()
    t.update(cambio)
    errs = errores(zip_tema(tema=t, css=None))
    assert any(fragmento in e for e in errs), errs


def _valores(**v):
    t = tema_dict()
    t["valores"].update(v)
    return t


@pytest.mark.parametrize("valores", [
    {"colores": {"fondo": "red"}},
    {"colores": {"fondo": "#fff"}},
    {"colores": {"inventado": "#ffffff"}},
    {"fuente_titulo": "comic-sans"},
    {"radio_tarjeta": 31},
    {"radio_tarjeta": True},
    {"forma_sello": "estrella"},
    {"sombra": "si"},
    {"fondo_velo": 81},
    {"campo_raro": 1},
])
def test_tema_json_valores_fuera_de_lista(valores):
    assert errores(zip_tema(tema=_valores(**valores), css=None))


def test_tema_json_claves_duplicadas():
    z = hacer_zip({"tema.json": b'{"formato":1,"formato":1}'})
    assert any("duplicada" in e for e in errores(z))


def test_fondo_declarado_pero_ausente_y_viceversa():
    t = tema_dict(fondo={"archivo": "fondo.webp"})
    assert any("no lo contiene" in e for e in errores(zip_tema(tema=t, css=None)))
    z = hacer_zip({"tema.json": json.dumps(tema_dict()).encode(), "fondo.webp": webp(50, 50)})
    assert any("no lo declara" in e for e in errores(z))


def test_fondo_png_falso():
    errs = errores(zip_tema(css=None, fondo=("fondo.png", b"<html>no soy png</html>")))
    assert any("imagen" in e for e in errs)
