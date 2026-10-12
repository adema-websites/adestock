import io
import re
import time

import pytest

from adestock_temas import auth
from adestock_temas.web import crear_app
from conftest import PASSWORD, codigo_totp, tema_dict, webp, zip_tema

H = {"Host": "127.0.0.1:8765"}


@pytest.fixture
def cliente(env, cuenta):
    app = crear_app(env, puerto=8765)
    app.testing = True
    return app.test_client()


def csrf_de(html):
    return re.search(r'name="csrf" value="([^"]+)"', html).group(1)


def entrar(c, secreto, desplazamiento=0, password=PASSWORD):
    r = c.get("/login", headers=H)
    return c.post("/login", data={"csrf": csrf_de(r.text), "password": password,
                                  "codigo": codigo_totp(secreto, desplazamiento)}, headers=H)


def token(c):
    return csrf_de(c.get("/subir", headers=H).text)


def test_subida_sin_sesion_es_rechazada_y_no_escribe_nada(env, cliente):
    r = cliente.post("/subir", data={"zip": (io.BytesIO(zip_tema(css=None)), "t.zip")}, headers=H,
                     content_type="multipart/form-data")
    assert r.status_code == 401
    assert not env.api.exists() and not env.catalogo.exists()
    assert not (env.estado / "staging").exists()
    for ruta in ("/", "/subir", "/auditoria", "/verificar"):
        r = cliente.get(ruta, headers=H)
        assert r.status_code == 302 and "/login" in r.headers["Location"]
    for ruta in ("/publicar/abcdefghijklmnop", "/tema/navidad-dorado", "/backup", "/logout"):
        assert cliente.post(ruta, data={}, headers=H).status_code == 401


def test_no_hay_endpoint_publico_de_subida_en_el_sitio_estatico():
    from pathlib import Path
    api = Path(__file__).resolve().parents[2] / "api" / "temas-revista"
    for f in api.rglob("*"):
        assert f.suffix in {"", ".json", ".sig", ".zip", ".webp"}, f


def test_login_correcto_y_totp_no_reutilizable(env, cuenta, cliente):
    r = entrar(cliente, cuenta[1])
    assert r.status_code == 302
    assert cliente.get("/", headers=H).status_code == 200
    otro = crear_app(env, puerto=8765).test_client()
    r = entrar(otro, cuenta[1])                          # mismo código TOTP, ya usado
    assert r.status_code == 401


def test_login_con_password_o_codigo_incorrecto(cliente, cuenta):
    assert entrar(cliente, cuenta[1], password="Incorrecta#12345678").status_code == 401
    r = cliente.get("/login", headers=H)
    r = cliente.post("/login", data={"csrf": csrf_de(r.text), "password": PASSWORD, "codigo": "000000"}, headers=H)
    assert r.status_code == 401


def test_bloqueo_tras_5_intentos_aun_con_credenciales_correctas(cliente, cuenta):
    for _ in range(5):
        assert entrar(cliente, cuenta[1], password="Incorrecta#12345678").status_code == 401
    r = entrar(cliente, cuenta[1])
    assert r.status_code == 429


def test_bloqueo_expira(env, cuenta):
    cred = auth.Credenciales(env.estado)
    ahora = time.time()
    for i in range(5):
        cred.registrar_fallo(ahora - 20 * 60 + i)
    assert cred.segundos_bloqueo(ahora) == 0           # fuera de la ventana de 15 min


def test_csrf_obligatorio(cliente, cuenta):
    entrar(cliente, cuenta[1])
    assert cliente.post("/backup", data={}, headers=H).status_code == 403
    assert cliente.post("/backup", data={"csrf": "falso"}, headers=H).status_code == 403
    assert cliente.post("/backup", data={"csrf": token(cliente)}, headers={**H, "Origin": "http://evil.com"}).status_code == 403


def test_host_ajeno_rechazado_anti_dns_rebinding(cliente):
    assert cliente.get("/login", headers={"Host": "evil.com"}).status_code == 400


def test_sesion_expira_por_inactividad(env, cuenta, monkeypatch):
    app = crear_app(env, puerto=8765)
    c = app.test_client()
    entrar(c, cuenta[1])
    assert c.get("/", headers=H).status_code == 200
    real = time.time
    monkeypatch.setattr(time, "time", lambda: real() + 31 * 60)
    r = c.get("/", headers=H)
    assert r.status_code == 302 and "/login" in r.headers["Location"]


def test_cabeceras_de_seguridad_y_cookie(cliente):
    r = cliente.get("/login", headers=H)
    assert "default-src 'none'" in r.headers["Content-Security-Policy"]
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    cookie = r.headers["Set-Cookie"]
    assert "HttpOnly" in cookie and "SameSite=Strict" in cookie


def test_flujo_completo_subir_confirmar_publicar(env, cuenta, cliente):
    entrar(cliente, cuenta[1])
    datos = {"csrf": token(cliente), "zip": (io.BytesIO(zip_tema(css=None)), "t.zip"),
             "miniatura": (io.BytesIO(webp()), "m.webp"), "etiquetas": "navidad, fiestas",
             "formatos": ["a4", "post"]}
    r = cliente.post("/subir", data=datos, headers=H, content_type="multipart/form-data")
    assert r.status_code == 302
    url = r.headers["Location"]
    page = cliente.get(url, headers=H).text
    assert "El ZIP cumple el contrato" in page
    tok = url.rsplit("/", 1)[1]
    # contraseña incorrecta → no publica
    r = cliente.post(f"/publicar/{tok}", data={"csrf": csrf_de(page), "password": "mal"}, headers=H)
    assert r.status_code == 302 and not (env.api / "index.json").exists()
    r = cliente.post(f"/publicar/{tok}", data={"csrf": csrf_de(page), "password": PASSWORD}, headers=H)
    assert r.status_code == 200 and "Publicado" in r.text
    assert (env.api / "index.json").exists() and (env.api / "index.json.sig").exists()
    aud = cliente.get("/auditoria", headers=H).text
    assert "publicado" in aud and "login_ok" in aud


def test_subida_invalida_muestra_el_motivo_y_no_publica(env, cuenta, cliente):
    entrar(cliente, cuenta[1])
    malo = zip_tema(css=".card{background:url(http://evil/x.png)}")
    r = cliente.post("/subir", data={"csrf": token(cliente), "zip": (io.BytesIO(malo), "t.zip"),
                                     "miniatura": (io.BytesIO(webp()), "m.webp"), "formatos": ["a4"]},
                     headers=H, content_type="multipart/form-data")
    assert r.status_code == 422 and "url()" in r.text
    assert not env.api.exists()


def test_politica_de_password():
    assert auth.validar_politica_password("corta")
    assert auth.validar_politica_password("soloMinusculasyLargas")
    assert not auth.validar_politica_password("Larga-Y-Segura#2026")
