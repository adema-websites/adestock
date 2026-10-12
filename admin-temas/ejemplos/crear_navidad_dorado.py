"""Genera el tema de ejemplo «Navidad dorado» (ZIP + miniatura + captura) en la carpeta indicada.

Uso: python ejemplos/crear_navidad_dorado.py <carpeta_salida>
La miniatura/captura son ilustraciones generadas, NO capturas reales de una hoja A4:
reemplazalas por capturas del Adestock cuando puedas (subiendo una versión nueva).
"""
import json
import random
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

VERDE, VERDE_OSC, ORO, CREMA = (11, 61, 46), (7, 42, 32), (245, 197, 66), (255, 250, 240)

TEMA = {
    "formato": 1, "producto": "adestock-revista-tema", "id": "navidad-dorado", "nombre": "Navidad dorado",
    "descripcion": "Fondo verde oscuro con detalles dorados para ofertas de fin de año.",
    "autor": "ADEMA Sistemas", "version": "1.0.0", "base": "oscuro",
    "valores": {
        "colores": {
            "fondo": "#0b3d2e", "cabecera_fondo": "#0b3d2e", "cabecera_texto": "#ffffff", "titulo": "#f5c542",
            "tarjeta": "#fffaf0", "texto": "#1b1b1b", "texto_suave": "#5c5c5c", "precio": "#b3122a",
            "promo": "#0b3d2e", "sello_fondo": "#b3122a", "sello_texto": "#ffffff", "franja_fondo": "#f5c542",
            "franja_texto": "#0b3d2e", "vigencia_fondo": "#f5c542", "vigencia_texto": "#0b3d2e",
            "pie_fondo": "#072a20", "pie_texto": "#e8e0c8"},
        "fuente_titulo": "fraunces", "fuente_texto": "barlow", "fuente_precio": "archivo",
        "radio_tarjeta": 14, "forma_sello": "circulo", "sello_inclinado": True, "sombra": True, "fondo_velo": 20},
    "fondo": {"archivo": "fondo.webp"},
}

CSS = """/* Navidad dorado: solo selectores y propiedades de la lista blanca */
.hoja { background-image: linear-gradient(180deg, var(--t-bg) 0%, #072a20 100%); }
.h-cab { border-bottom: 4px solid #f5c542; }
.h-titulo { text-shadow: 0 0.3cqw 0 rgba(0, 0, 0, 0.35); letter-spacing: 0.02em; }
.card { position: relative; border: 2px solid #f5c542; box-shadow: 0 6px 14px rgba(0, 0, 0, 0.35); }
.card::before { content: "❄"; position: absolute; top: 4px; right: 8px; color: #f5c542; font-size: 3cqw; z-index: 2; }
.sello { border: 2px dashed #ffffff; }
.precio-zona { background: linear-gradient(90deg, #fffaf0, #f5e6b8); border-radius: 8px; padding: 1cqw; }
.h-pie { border-top: 3px double #f5c542; }
.ribbon::after { content: "★"; color: #0b3d2e; margin-left: 1cqw; }
"""

INSTRUCCIONES = """# Navidad dorado: guía para pedir variantes a una IA

Este tema usa el formato 1 de temas de revista de Adestock.
- Solo se permiten los campos de tema.json del contrato (colores #rrggbb, 5 fuentes cerradas).
- tema.css: sin url(), @import, @media, @keyframes, !important ni position: fixed; solo clases de la hoja.
- No cambies el id si querés una variante: creá otro id y una versión 1.0.0.
"""


def fondo(ruta: Path):
    w, h = 1588, 2246
    im = Image.new("RGB", (w, h))
    px = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        px.line([(0, y), (w, y)], fill=tuple(int(VERDE[i] * (1 - t) + VERDE_OSC[i] * t) for i in range(3)))
    rnd = random.Random(7)
    for _ in range(260):
        x, y, r = rnd.randrange(w), rnd.randrange(h), rnd.choice((2, 3, 4, 6))
        px.ellipse([x - r, y - r, x + r, y + r], fill=(200, 160, 60))
    im.save(ruta, "WEBP", quality=60)


def hoja_ilustrada(ruta: Path, w: int, h: int):
    im = Image.new("RGB", (w, h), VERDE)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, int(h * 0.16)], fill=VERDE)
    d.rectangle([0, int(h * 0.16), w, int(h * 0.16) + 5], fill=ORO)
    d.rectangle([w * 0.08, h * 0.05, w * 0.6, h * 0.11], fill=ORO)
    cols, filas = 3, 3
    cw, ch = (w * 0.86) / cols, (h * 0.78) / filas
    for i in range(cols * filas):
        x0 = w * 0.07 + (i % cols) * cw + 4
        y0 = h * 0.2 + (i // cols) * ch + 4
        d.rounded_rectangle([x0, y0, x0 + cw - 8, y0 + ch - 8], radius=10, fill=CREMA, outline=ORO, width=2)
        d.rectangle([x0 + 10, y0 + ch * 0.66, x0 + cw * 0.5, y0 + ch * 0.82], fill=(179, 18, 42))
        d.ellipse([x0 + cw * 0.3, y0 + 12, x0 + cw * 0.7, y0 + ch * 0.55], fill=(235, 226, 200))
    im.save(ruta, "WEBP", quality=75)


def main(salida: Path):
    salida.mkdir(parents=True, exist_ok=True)
    fondo(salida / "fondo.webp")
    hoja_ilustrada(salida / "vista-previa.webp", 600, 848)
    hoja_ilustrada(salida / "miniatura.webp", 600, 424)
    hoja_ilustrada(salida / "vista-1.webp", 600, 848)
    ruta_zip = salida / "navidad-dorado-1.0.0.zip"
    fijo = (2026, 10, 10, 0, 0, 0)       # fecha fija: el ZIP sale siempre igual
    with zipfile.ZipFile(ruta_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        contenidos = {
            "tema.json": json.dumps(TEMA, ensure_ascii=False, indent=2).encode("utf-8"),
            "tema.css": CSS.encode("utf-8"),
            "fondo.webp": (salida / "fondo.webp").read_bytes(),
            "vista-previa.webp": (salida / "vista-previa.webp").read_bytes(),
            "INSTRUCCIONES-PARA-IA.md": INSTRUCCIONES.encode("utf-8"),
        }
        for nombre, datos in contenidos.items():
            zi = zipfile.ZipInfo(nombre, fijo)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o100644 << 16
            zf.writestr(zi, datos)
    print(ruta_zip, ruta_zip.stat().st_size, "bytes")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
