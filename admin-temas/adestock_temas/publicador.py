"""Catálogo, publicación inmutable, generación y firma de index.json, verificación e integridad."""
import hashlib
import json
import os
import re
import shutil
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import config as C
from . import firma as F
from .config import Entorno
from .validador import (Resultado, validar_etiquetas, validar_formatos, validar_imagen_tienda, validar_zip)

TZ_AR = timezone(timedelta(hours=-3))
CLAVES_INDICE = ("id", "nombre", "descripcion", "autor", "version", "premium", "etiquetas", "formatos",
                 "miniatura", "capturas", "zip", "bytes", "sha256", "requiere_formato", "publicado")


class PublicacionError(Exception):
    """Error de reglas de publicación (no de validación del ZIP)."""


def ahora() -> datetime:
    return datetime.now(TZ_AR)


def semver(v: str):
    return tuple(int(x) for x in v.split("."))


def escribir_atomico(ruta: Path, datos: bytes):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta.with_name(ruta.name + ".tmp")
    tmp.write_bytes(datos)
    os.replace(tmp, ruta)


# ------------------------------------------------------------------ catálogo

def cargar_catalogo(env: Entorno) -> dict:
    if not env.catalogo.exists():
        return {"formato": 1, "temas": {}}
    return json.loads(env.catalogo.read_text(encoding="utf-8"))


def guardar_catalogo(env: Entorno, cat: dict):
    escribir_atomico(env.catalogo, (json.dumps(cat, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())


def ultima_version(entrada: dict) -> dict:
    return max(entrada["versiones"], key=lambda v: semver(v["version"]))


def construir_indice(cat: dict, momento: datetime) -> dict:
    temas = []
    for tid, t in cat["temas"].items():
        if t.get("retirado") or not t["versiones"]:
            continue
        v = ultima_version(t)
        temas.append({
            "id": tid, "nombre": v["nombre"], "descripcion": v["descripcion"], "autor": v["autor"],
            "version": v["version"], "premium": bool(t.get("premium", False)),
            "etiquetas": list(t["etiquetas"]), "formatos": list(t["formatos"]),
            "miniatura": t["miniatura"], "capturas": list(t.get("capturas", [])),
            "zip": v["zip"], "bytes": v["bytes"], "sha256": v["sha256"],
            "requiere_formato": v["requiere_formato"], "publicado": v["publicado"],
        })
    temas.sort(key=lambda x: (x["publicado"], x["id"]), reverse=True)
    return {"formato": 1, "actualizado": momento.isoformat(timespec="seconds"), "temas": temas}


def serializar_indice(indice: dict) -> bytes:
    return (json.dumps(indice, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


# ------------------------------------------------------------------ preparación (validación)

@dataclass
class Preparacion:
    errores: list = field(default_factory=list)
    avisos: list = field(default_factory=list)
    zip_bytes: bytes = b""
    resultado: Resultado = None
    miniatura: bytes = None
    capturas: list = field(default_factory=list)
    etiquetas: list = field(default_factory=list)
    formatos: list = field(default_factory=list)
    premium: bool = False
    tema_id: str = ""
    version: str = ""
    es_nuevo: bool = True
    anterior: str = ""

    @property
    def ok(self) -> bool:
        return not self.errores


def preparar(env: Entorno, zip_bytes: bytes, miniatura: bytes, capturas: list, etiquetas: list,
             formatos: list, premium: bool = False) -> Preparacion:
    p = Preparacion(zip_bytes=zip_bytes, miniatura=miniatura or None, capturas=capturas or [],
                    etiquetas=etiquetas, formatos=formatos, premium=bool(premium))
    res = validar_zip(zip_bytes)
    p.resultado = res
    p.errores.extend(res.errores)
    validar_etiquetas(etiquetas, p.errores)
    validar_formatos(formatos, p.errores)
    if p.capturas and len(p.capturas) > C.CAPTURAS_MAX:
        p.errores.append(f"Máximo {C.CAPTURAS_MAX} capturas.")
    if p.miniatura:
        validar_imagen_tienda(p.miniatura, "miniatura", C.MINIATURA_MAX_BYTES, p.errores)
    for i, cap in enumerate(p.capturas, 1):
        validar_imagen_tienda(cap, f"captura {i}", C.CAPTURA_MAX_BYTES, p.errores)
    if not res.ok:
        return p
    tema = res.tema
    p.tema_id, p.version = tema["id"], tema["version"]
    cat = cargar_catalogo(env)
    ent = cat["temas"].get(p.tema_id)
    if ent is None:
        if not p.miniatura:
            p.errores.append("Un tema nuevo necesita miniatura (WebP).")
        carpeta_id = env.api / p.tema_id
        if carpeta_id.exists() and any(carpeta_id.iterdir()):
            p.errores.append(f"El id «{p.tema_id}» ya tiene archivos publicados: los ids nunca se reutilizan.")
    else:
        p.es_nuevo = False
        if ent.get("retirado"):
            p.errores.append(f"El tema «{p.tema_id}» está retirado. Restauralo primero para publicar versiones nuevas.")
        p.anterior = ultima_version(ent)["version"]
        if semver(p.version) <= semver(p.anterior):
            p.errores.append(f"La versión {p.version} debe ser MAYOR que la última publicada ({p.anterior}). "
                             "Las versiones publicadas son inmutables.")
        if any(v["version"] == p.version for v in ent["versiones"]):
            p.errores.append(f"La versión {p.version} ya fue publicada y no se puede reemplazar.")
    if (env.api / p.tema_id / f"{p.tema_id}-{p.version}.zip").exists():
        p.errores.append("Ya existe un ZIP con ese id y versión: no se reemplaza nunca.")
    return p


# ------------------------------------------------------------------ publicación

def snapshot(env: Entorno, etiqueta: str):
    """Copia índice, firma, catálogo y auditoría antes de cada cambio (últimas 50)."""
    destino = env.estado / "backups" / "snapshots" / f"{ahora():%Y%m%d-%H%M%S}-{etiqueta}"
    destino.mkdir(parents=True, exist_ok=True)
    for src in (env.api / "index.json", env.api / "index.json.sig", env.catalogo, env.auditoria):
        if src.exists():
            shutil.copy2(src, destino / src.name)
    snaps = sorted((env.estado / "backups" / "snapshots").iterdir())
    for viejo in snaps[:-50]:
        shutil.rmtree(viejo, ignore_errors=True)


def regenerar_indice(env: Entorno, cat: dict, priv) -> dict:
    indice = construir_indice(cat, ahora())
    cuerpo = serializar_indice(indice)
    escribir_atomico(env.api / "index.json", cuerpo)
    escribir_atomico(env.api / "index.json.sig", (F.firmar(priv, cuerpo) + "\n").encode("ascii"))
    return indice


def publicar(env: Entorno, p: Preparacion, priv) -> dict:
    """Escribe ZIP (exclusivo), imágenes, catálogo, índice y firma. Revierte todo si algo falla."""
    if not p.ok:
        raise PublicacionError("La preparación tiene errores; no se publica.")
    snapshot(env, f"pre-{p.tema_id}-{p.version}")
    carpeta = env.api / p.tema_id
    creados, previos = [], {}
    cat_antes = env.catalogo.read_bytes() if env.catalogo.exists() else None
    idx_antes = {n: (env.api / n).read_bytes() for n in ("index.json", "index.json.sig") if (env.api / n).exists()}
    carpeta_nueva = not carpeta.exists()
    try:
        carpeta.mkdir(parents=True, exist_ok=True)
        ruta_zip = carpeta / f"{p.tema_id}-{p.version}.zip"
        with open(ruta_zip, "xb") as fh:           # 'x': falla si existe → nunca pisa una versión
            creados.append(ruta_zip)
            fh.write(p.zip_bytes)
        # relectura: lo escrito en disco es lo que se hasheó
        if hashlib.sha256(ruta_zip.read_bytes()).hexdigest() != p.resultado.sha256:
            raise PublicacionError("El ZIP escrito no coincide con el validado.")

        def poner(ruta: Path, datos: bytes):
            if ruta.exists():
                previos[ruta] = ruta.read_bytes()
            else:
                creados.append(ruta)
            escribir_atomico(ruta, datos)

        cat = cargar_catalogo(env)
        ent = cat["temas"].setdefault(p.tema_id, {
            "retirado": False, "premium": p.premium, "etiquetas": p.etiquetas, "formatos": p.formatos,
            "miniatura": f"{p.tema_id}/miniatura.webp", "capturas": [], "versiones": []})
        if p.miniatura:
            poner(carpeta / "miniatura.webp", p.miniatura)
        if p.capturas:
            for viejo in ent.get("capturas", []):
                ruta_v = env.api / viejo
                if ruta_v.exists():
                    previos[ruta_v] = ruta_v.read_bytes()
                    ruta_v.unlink()
            ent["capturas"] = []
            for i, cap in enumerate(p.capturas, 1):
                poner(carpeta / f"vista-{i}.webp", cap)
                ent["capturas"].append(f"{p.tema_id}/vista-{i}.webp")
        t = p.resultado.tema
        ent["etiquetas"], ent["formatos"], ent["premium"] = p.etiquetas, p.formatos, p.premium
        ent["versiones"].append({
            "version": p.version, "nombre": t["nombre"], "descripcion": t["descripcion"], "autor": t["autor"],
            "zip": f"{p.tema_id}/{p.tema_id}-{p.version}.zip", "bytes": p.resultado.bytes,
            "sha256": p.resultado.sha256, "requiere_formato": t["formato"],
            "publicado": ahora().date().isoformat(),
        })
        guardar_catalogo(env, cat)
        return regenerar_indice(env, cat, priv)
    except BaseException:
        for ruta in creados:
            ruta.unlink(missing_ok=True)
        if carpeta_nueva and carpeta.exists() and not any(carpeta.iterdir()):
            carpeta.rmdir()
        for ruta, datos in previos.items():
            escribir_atomico(ruta, datos)
        if cat_antes is None:
            env.catalogo.unlink(missing_ok=True)
        else:
            escribir_atomico(env.catalogo, cat_antes)
        for n, datos in idx_antes.items():
            escribir_atomico(env.api / n, datos)
        raise


def editar_meta(env: Entorno, tema_id: str, etiquetas: list, formatos: list, premium: bool, priv) -> dict:
    errores = []
    validar_etiquetas(etiquetas, errores)
    validar_formatos(formatos, errores)
    if errores:
        raise PublicacionError(" ".join(errores))
    cat = cargar_catalogo(env)
    if tema_id not in cat["temas"]:
        raise PublicacionError("Tema inexistente.")
    snapshot(env, f"meta-{tema_id}")
    ent = cat["temas"][tema_id]
    ent["etiquetas"], ent["formatos"], ent["premium"] = etiquetas, formatos, bool(premium)
    guardar_catalogo(env, cat)
    return regenerar_indice(env, cat, priv)


def cambiar_retiro(env: Entorno, tema_id: str, retirar: bool, priv) -> dict:
    cat = cargar_catalogo(env)
    if tema_id not in cat["temas"]:
        raise PublicacionError("Tema inexistente.")
    snapshot(env, f"{'retiro' if retirar else 'restauro'}-{tema_id}")
    cat["temas"][tema_id]["retirado"] = bool(retirar)   # los ZIP no se borran jamás
    guardar_catalogo(env, cat)
    return regenerar_indice(env, cat, priv)


# ------------------------------------------------------------------ verificación

def verificar_publicacion(env: Entorno, clave_publica_b64: str = None) -> list:
    """Recalcula sha256/bytes de cada ZIP publicado, re-valida su contenido y comprueba la firma del índice."""
    problemas = []
    ruta_idx = env.api / "index.json"
    if not ruta_idx.exists():
        return ["No existe index.json."]
    cuerpo = ruta_idx.read_bytes()
    try:
        indice = json.loads(cuerpo)
    except ValueError:
        return ["index.json no es JSON válido."]
    cat = cargar_catalogo(env)
    for t in indice.get("temas", []):
        if list(t.keys()) != list(CLAVES_INDICE):
            problemas.append(f"{t.get('id')}: campos del índice distintos al contrato.")
        for ruta in [t["miniatura"], t["zip"], *t.get("capturas", [])]:
            if ruta.startswith(("/", "http")) or ".." in ruta or "\\" in ruta:
                problemas.append(f"{t['id']}: ruta insegura «{ruta}».")
        z = env.api / t["zip"]
        if not z.exists():
            problemas.append(f"{t['id']}: falta {t['zip']}.")
            continue
        datos = z.read_bytes()
        if len(datos) != t["bytes"]:
            problemas.append(f"{t['id']}: bytes no coinciden ({len(datos)} ≠ {t['bytes']}).")
        if hashlib.sha256(datos).hexdigest() != t["sha256"]:
            problemas.append(f"{t['id']}: sha256 no coincide con el ZIP publicado.")
        r = validar_zip(datos)
        problemas.extend(f"{t['id']}: {e}" for e in r.errores)
        for ruta in [t["miniatura"], *t.get("capturas", [])]:
            if not (env.api / ruta).exists():
                problemas.append(f"{t['id']}: falta {ruta}.")
    # todo ZIP del catálogo debe seguir intacto (también los de versiones viejas y temas retirados)
    for tid, ent in cat["temas"].items():
        for v in ent["versiones"]:
            z = env.api / v["zip"]
            if not z.exists():
                problemas.append(f"{tid} {v['version']}: ZIP desaparecido.")
            elif hashlib.sha256(z.read_bytes()).hexdigest() != v["sha256"]:
                problemas.append(f"{tid} {v['version']}: el ZIP publicado fue modificado.")
    ruta_sig = env.api / "index.json.sig"
    if clave_publica_b64:
        if not ruta_sig.exists():
            problemas.append("Falta index.json.sig.")
        elif not F.verificar(clave_publica_b64, cuerpo, ruta_sig.read_text()):
            problemas.append("La firma de index.json NO es válida para la clave pública indicada.")
    return problemas


# ------------------------------------------------------------------ backup

def hacer_backup(env: Entorno, destino: Path = None) -> Path:
    destino = destino or (env.estado / "backups")
    destino.mkdir(parents=True, exist_ok=True)
    out = destino / f"adestock-temas-{ahora():%Y%m%d-%H%M%S}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        if env.api.exists():
            for f in sorted(env.api.rglob("*")):
                if f.is_file():
                    zf.write(f, "api/temas-revista/" + f.relative_to(env.api).as_posix())
        for extra, nombre in ((env.catalogo, "catalogo.json"), (env.auditoria, "auditoria.jsonl")):
            if extra.exists():
                zf.write(extra, nombre)
    return out
