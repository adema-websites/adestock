"""Firma Ed25519 del índice. La clave privada vive cifrada en el directorio de estado (fuera del repo)."""
import base64
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


def _ruta(estado: Path) -> Path:
    return estado / "firma_ed25519.pem"


def existe_clave(estado: Path) -> bool:
    return _ruta(estado).exists()


def generar_clave(estado: Path, password: str) -> str:
    """Crea la clave privada cifrada. Devuelve la pública (base64 raw, 32 bytes)."""
    estado.mkdir(parents=True, exist_ok=True)
    ruta = _ruta(estado)
    if ruta.exists():
        raise FileExistsError("Ya existe una clave de firma; usá «rotar-clave».")
    priv = Ed25519PrivateKey.generate()
    pem = priv.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                             serialization.BestAvailableEncryption(password.encode("utf-8")))
    ruta.write_bytes(pem)
    pub = publica_b64(priv.public_key())
    (estado / "clave_publica.txt").write_text(pub + "\n", encoding="utf-8")
    return pub


def cargar_privada(estado: Path, password: str) -> Ed25519PrivateKey:
    try:
        return serialization.load_pem_private_key(_ruta(estado).read_bytes(), password.encode("utf-8"))
    except (ValueError, TypeError) as exc:
        raise ValueError("No se pudo abrir la clave de firma (¿contraseña incorrecta?).") from exc


def publica_b64(pub: Ed25519PublicKey) -> str:
    raw = pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode("ascii")


def publica_pem(pub_b64: str) -> str:
    pub = Ed25519PublicKey.from_public_bytes(base64.b64decode(pub_b64))
    return pub.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()


def firmar(priv: Ed25519PrivateKey, contenido: bytes) -> str:
    return base64.b64encode(priv.sign(contenido)).decode("ascii")


def verificar(pub_b64: str, contenido: bytes, firma_b64: str) -> bool:
    try:
        pub = Ed25519PublicKey.from_public_bytes(base64.b64decode(pub_b64.strip(), validate=True))
        pub.verify(base64.b64decode(firma_b64.strip(), validate=True), contenido)
        return True
    except (InvalidSignature, ValueError):
        return False


def rotar(estado: Path, password: str) -> str:
    """Archiva la clave actual (privada cifrada + pública) y crea una nueva. Devuelve la nueva pública."""
    ruta = _ruta(estado)
    if ruta.exists():
        arch = estado / "claves-anteriores"
        arch.mkdir(exist_ok=True)
        sufijo = len(list(arch.glob("*.pem"))) + 1
        ruta.replace(arch / f"firma_ed25519.{sufijo}.pem")
        pub = estado / "clave_publica.txt"
        if pub.exists():
            pub.replace(arch / f"clave_publica.{sufijo}.txt")
    return generar_clave(estado, password)


def recifrar(estado: Path, vieja: str, nueva: str):
    priv = cargar_privada(estado, vieja)
    pem = priv.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                             serialization.BestAvailableEncryption(nueva.encode("utf-8")))
    _ruta(estado).write_bytes(pem)
