"""Registro de auditoría: JSON por línea, encadenado con hash (detecta ediciones/borrados)."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

GENESIS = "0" * 64


def _hash(prev: str, cuerpo: dict) -> str:
    return hashlib.sha256((prev + json.dumps(cuerpo, sort_keys=True, ensure_ascii=False)).encode()).hexdigest()


def _ultimo_hash(ruta: Path) -> str:
    if not ruta.exists():
        return GENESIS
    ultimo = GENESIS
    with ruta.open("r", encoding="utf-8") as fh:
        for linea in fh:
            if linea.strip():
                ultimo = json.loads(linea)["hash"]
    return ultimo


def registrar(archivo_log: Path, evento: str, usuario: str = "admin", ip: str = "-", **datos):
    ruta = archivo_log
    ruta.parent.mkdir(parents=True, exist_ok=True)
    cuerpo = {"cuando": datetime.now(timezone.utc).isoformat(timespec="seconds"), "quien": usuario,
              "ip": ip, "evento": evento, **datos}
    prev = _ultimo_hash(ruta)
    cuerpo = {**cuerpo, "prev": prev}
    cuerpo["hash"] = _hash(prev, {k: v for k, v in cuerpo.items() if k != "hash"})
    with ruta.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(cuerpo, ensure_ascii=False, sort_keys=True) + "\n")


def leer(ruta: Path, ultimos: int = 200):
    if not ruta.exists():
        return []
    with ruta.open("r", encoding="utf-8") as fh:
        filas = [json.loads(x) for x in fh if x.strip()]
    return filas[-ultimos:][::-1]


def verificar_cadena(ruta: Path) -> bool:
    prev = GENESIS
    if not ruta.exists():
        return True
    with ruta.open("r", encoding="utf-8") as fh:
        for linea in fh:
            if not linea.strip():
                continue
            fila = json.loads(linea)
            h = fila.pop("hash")
            if fila.get("prev") != prev or _hash(prev, fila) != h:
                return False
            prev = h
    return True
