import hashlib
import json

import pytest

from adestock_temas import auditoria as A
from adestock_temas import firma
from adestock_temas import publicador as P
from conftest import tema_dict, webp, zip_tema

FORMATOS = ["a4", "a4h", "post", "postv", "historia"]


def preparar(env, version="1.0.0", tid="navidad-dorado", mini=True, premium=False, **kw):
    t = tema_dict(version=version, id=tid)
    return P.preparar(env, zip_tema(tema=t, css=None), webp() if mini else None, [], ["navidad"], FORMATOS, premium)


def publicar(env, priv, **kw):
    p = preparar(env, **kw)
    assert p.ok, p.errores
    return P.publicar(env, p, priv)


def test_indice_respeta_el_contrato_y_la_huella(env, priv, cuenta):
    publicar(env, priv)
    cuerpo = (env.api / "index.json").read_bytes()
    idx = json.loads(cuerpo)
    assert list(idx) == ["formato", "actualizado", "temas"] and idx["formato"] == 1
    t = idx["temas"][0]
    assert list(t) == list(P.CLAVES_INDICE)
    zip_ruta = env.api / t["zip"]
    assert t["zip"] == "navidad-dorado/navidad-dorado-1.0.0.zip"
    assert t["sha256"] == hashlib.sha256(zip_ruta.read_bytes()).hexdigest()
    assert t["bytes"] == zip_ruta.stat().st_size
    assert t["premium"] is False and t["requiere_formato"] == 1
    assert t["miniatura"] == "navidad-dorado/miniatura.webp"
    assert idx["actualizado"].endswith("-03:00")
    sig = (env.api / "index.json.sig").read_text()
    assert firma.verificar(cuenta[2], cuerpo, sig)
    assert P.verificar_publicacion(env, cuenta[2]) == []


def test_firma_no_valida_con_otra_clave_ni_con_indice_alterado(env, priv, cuenta, tmp_path):
    publicar(env, priv)
    cuerpo = (env.api / "index.json").read_bytes()
    sig = (env.api / "index.json.sig").read_text()
    otra = firma.generar_clave(tmp_path / "otro", "Otra-Clave#12345678")
    assert not firma.verificar(otra, cuerpo, sig)
    assert not firma.verificar(cuenta[2], cuerpo.replace(b"navidad", b"hackead"), sig)


def test_version_publicada_es_inmutable(env, priv):
    publicar(env, priv)
    # misma versión → rechazada
    p = preparar(env, version="1.0.0")
    assert not p.ok and any("MAYOR" in e or "ya fue publicada" in e or "no se reemplaza" in e for e in p.errores)
    # versión menor → rechazada
    p = preparar(env, version="0.9.0")
    assert not p.ok
    # el ZIP en disco no cambió
    antes = (env.api / "navidad-dorado" / "navidad-dorado-1.0.0.zip").read_bytes()
    publicar(env, priv, version="1.1.0", mini=False)
    assert (env.api / "navidad-dorado" / "navidad-dorado-1.0.0.zip").read_bytes() == antes
    assert (env.api / "navidad-dorado" / "navidad-dorado-1.1.0.zip").exists()
    idx = json.loads((env.api / "index.json").read_text())
    assert [t["version"] for t in idx["temas"]] == ["1.1.0"]


def test_comparacion_semantica_de_versiones(env, priv):
    publicar(env, priv, version="1.9.0")
    assert preparar(env, version="1.10.0", mini=False).ok       # 1.10.0 > 1.9.0 (no es orden de texto)


def test_tema_nuevo_exige_miniatura(env, priv):
    p = preparar(env, mini=False)
    assert not p.ok and any("miniatura" in e for e in p.errores)


def test_id_no_se_reutiliza(env, priv):
    publicar(env, priv)
    P.cambiar_retiro(env, "navidad-dorado", True, priv)
    p = preparar(env, version="2.0.0", mini=False)
    assert not p.ok and any("retirado" in e for e in p.errores)
    # carpeta huérfana con ese id (sin catálogo) tampoco se reutiliza
    (env.api / "otro-tema").mkdir()
    (env.api / "otro-tema" / "viejo.zip").write_bytes(b"x")
    p = preparar(env, tid="otro-tema")
    assert not p.ok and any("nunca se reutilizan" in e for e in p.errores)


def test_retirar_saca_del_indice_pero_no_borra_el_zip(env, priv, cuenta):
    publicar(env, priv)
    zip_ruta = env.api / "navidad-dorado" / "navidad-dorado-1.0.0.zip"
    huella = zip_ruta.read_bytes()
    idx = P.cambiar_retiro(env, "navidad-dorado", True, priv)
    assert idx["temas"] == []
    assert zip_ruta.read_bytes() == huella
    assert P.verificar_publicacion(env, cuenta[2]) == []
    idx = P.cambiar_retiro(env, "navidad-dorado", False, priv)
    assert len(idx["temas"]) == 1


def test_premium_editable_y_false_por_defecto(env, priv):
    publicar(env, priv)
    idx = P.editar_meta(env, "navidad-dorado", ["navidad", "oro"], ["a4"], True, priv)
    assert idx["temas"][0]["premium"] is True and idx["temas"][0]["formatos"] == ["a4"]
    with pytest.raises(P.PublicacionError):
        P.editar_meta(env, "navidad-dorado", ["Mal Formato"], ["a4"], False, priv)
    with pytest.raises(P.PublicacionError):
        P.editar_meta(env, "navidad-dorado", [], ["bogus"], False, priv)


def test_sha256_que_no_coincide_se_detecta(env, priv, cuenta):
    publicar(env, priv)
    zip_ruta = env.api / "navidad-dorado" / "navidad-dorado-1.0.0.zip"
    zip_ruta.write_bytes(zip_ruta.read_bytes() + b"x")            # alguien toca el ZIP publicado
    problemas = P.verificar_publicacion(env, cuenta[2])
    assert any("sha256" in x for x in problemas) and any("bytes" in x for x in problemas)


def test_indice_con_sha256_falso_se_detecta(env, priv, cuenta):
    publicar(env, priv)
    ruta = env.api / "index.json"
    idx = json.loads(ruta.read_text())
    idx["temas"][0]["sha256"] = "0" * 64
    ruta.write_text(json.dumps(idx, indent=2) + "\n")
    problemas = P.verificar_publicacion(env, cuenta[2])
    assert any("sha256 no coincide" in x for x in problemas)
    assert any("firma" in x.lower() for x in problemas)           # y además la firma deja de valer


def test_rollback_si_falla_a_mitad(env, priv, monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("falla simulada")
    monkeypatch.setattr(P, "regenerar_indice", boom)
    p = preparar(env)
    with pytest.raises(RuntimeError):
        P.publicar(env, p, priv)
    assert not (env.api / "navidad-dorado" / "navidad-dorado-1.0.0.zip").exists()
    assert not (env.api / "navidad-dorado" / "miniatura.webp").exists()
    assert not env.catalogo.exists()
    assert preparar(env).ok                                         # la versión no quedó "quemada"


def test_backup_incluye_indice_zip_y_auditoria(env, priv):
    import zipfile
    publicar(env, priv)
    A.registrar(env.auditoria, "prueba")
    ruta = P.hacer_backup(env)
    nombres = zipfile.ZipFile(ruta).namelist()
    assert "api/temas-revista/index.json" in nombres
    assert "api/temas-revista/navidad-dorado/navidad-dorado-1.0.0.zip" in nombres
    assert "auditoria.jsonl" in nombres and "catalogo.json" in nombres


def test_auditoria_encadenada_detecta_alteracion(env):
    A.registrar(env.auditoria, "a", archivo="x")
    A.registrar(env.auditoria, "b", sha256="y")
    assert A.verificar_cadena(env.auditoria)
    env.auditoria.write_text(env.auditoria.read_text().replace('"a"', '"z"'))
    assert not A.verificar_cadena(env.auditoria)


def test_rotacion_de_clave(env, priv, cuenta):
    from conftest import PASSWORD
    publicar(env, priv)
    vieja = cuenta[2]
    nueva = firma.rotar(env.estado, PASSWORD)
    assert nueva != vieja and (env.estado / "claves-anteriores").exists()
    P.regenerar_indice(env, P.cargar_catalogo(env), firma.cargar_privada(env.estado, PASSWORD))
    assert P.verificar_publicacion(env, nueva) == []
    assert any("firma" in x.lower() for x in P.verificar_publicacion(env, vieja))
