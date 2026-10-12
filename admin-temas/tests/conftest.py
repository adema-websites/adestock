import copy
import io
import json
import sys
import time
import zipfile
from pathlib import Path

import pytest
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "ejemplos"))

import crear_navidad_dorado as ejemplo  # noqa: E402
from adestock_temas import auth, firma  # noqa: E402
from adestock_temas.auth import Credenciales  # noqa: E402
from adestock_temas.config import Entorno  # noqa: E402

PASSWORD = "Prueba-Larga#2026-zq"
CSS_OK = ejemplo.CSS


def webp(w=600, h=424, color=(10, 60, 40)) -> bytes:
    b = io.BytesIO()
    Image.new("RGB", (w, h), color).save(b, "WEBP", quality=70)
    return b.getvalue()


def hacer_zip(archivos: dict, extra=None) -> bytes:
    """archivos: {nombre: bytes}. extra: callback(zf) para entradas raras."""
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as zf:
        for n, d in archivos.items():
            zi = zipfile.ZipInfo(n, (2026, 10, 10, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o100644 << 16
            zf.writestr(zi, d)
        if extra:
            extra(zf)
    return b.getvalue()


def tema_dict(**cambios):
    t = copy.deepcopy(ejemplo.TEMA)
    t.pop("fondo", None)
    t.update(cambios)
    return t


def zip_tema(tema=None, css=CSS_OK, fondo=None, extra_archivos=None, extra=None) -> bytes:
    tema = copy.deepcopy(tema if tema is not None else tema_dict())
    archivos = {}
    if fondo is not None:
        nombre, datos = fondo
        tema["fondo"] = {"archivo": nombre}
        archivos[nombre] = datos
    archivos["tema.json"] = json.dumps(tema).encode()
    if css is not None:
        archivos["tema.css"] = css.encode() if isinstance(css, str) else css
    archivos.update(extra_archivos or {})
    return hacer_zip(archivos, extra)


@pytest.fixture
def env(tmp_path):
    e = Entorno(sitio=tmp_path / "sitio", estado=tmp_path / "estado", catalogo=tmp_path / "catalogo.json")
    e.sitio.mkdir()
    return e


@pytest.fixture
def cuenta(env):
    cred = Credenciales(env.estado)
    secreto = cred.crear(PASSWORD)
    pub = firma.generar_clave(env.estado, PASSWORD)
    return cred, secreto, pub


@pytest.fixture
def priv(env, cuenta):
    return firma.cargar_privada(env.estado, PASSWORD)


def codigo_totp(secreto, desplazamiento=0):
    return auth._codigo(secreto, int(time.time() // 30) + desplazamiento)
