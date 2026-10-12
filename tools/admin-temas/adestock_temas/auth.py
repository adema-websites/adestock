"""Credenciales del administrador único: contraseña (scrypt), 2FA TOTP (RFC 6238) y límite de intentos."""
import base64
import hashlib
import hmac
import json
import os
import secrets
import struct
import time
from pathlib import Path

PASSWORD_MIN = 14
MAX_FALLOS = 5
VENTANA_S = 15 * 60
BLOQUEO_S = 15 * 60
_SCRYPT = dict(n=2 ** 15, r=8, p=1, maxmem=96 * 1024 * 1024, dklen=32)


def _escribir_privado(ruta: Path, datos: dict):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta.with_name(ruta.name + ".tmp")
    tmp.write_text(json.dumps(datos, indent=2), encoding="utf-8")
    try:
        os.chmod(tmp, 0o600)
    except OSError:  # pragma: no cover (Windows)
        pass
    os.replace(tmp, ruta)


def validar_politica_password(pw: str):
    """Devuelve lista de problemas (vacía = ok)."""
    prob = []
    if len(pw) < PASSWORD_MIN:
        prob.append(f"Mínimo {PASSWORD_MIN} caracteres.")
    clases = sum(bool(x) for x in (any(c.islower() for c in pw), any(c.isupper() for c in pw),
                                    any(c.isdigit() for c in pw), any(not c.isalnum() for c in pw)))
    if clases < 3:
        prob.append("Combiná al menos 3 tipos: minúsculas, mayúsculas, números, símbolos.")
    if any(x in pw.lower() for x in ("adestock", "adema", "password", "contraseña", "123456")):
        prob.append("No uses palabras obvias (adestock, adema, password, 123456…).")
    return prob


def _hash_pw(pw: str, salt: bytes) -> str:
    return base64.b64encode(hashlib.scrypt(pw.encode("utf-8"), salt=salt, **_SCRYPT)).decode()


# ---------------------------------------------------------------- TOTP
def nuevo_secreto_totp() -> str:
    return base64.b32encode(secrets.token_bytes(20)).decode().rstrip("=")


def _codigo(secreto: str, contador: int) -> str:
    clave = base64.b32decode(secreto + "=" * (-len(secreto) % 8))
    mac = hmac.new(clave, struct.pack(">Q", contador), hashlib.sha1).digest()
    o = mac[-1] & 0x0F
    return f"{(struct.unpack('>I', mac[o:o + 4])[0] & 0x7FFFFFFF) % 1_000_000:06d}"


def uri_totp(secreto: str, cuenta: str = "admin", emisor: str = "Adestock Temas") -> str:
    return f"otpauth://totp/{emisor}:{cuenta}?secret={secreto}&issuer={emisor}&digits=6&period=30"


class Credenciales:
    def __init__(self, estado: Path):
        self.estado = estado
        self.ruta = estado / "admin.json"
        self.ruta_fallos = estado / "intentos.json"

    # -- alta
    def existe(self) -> bool:
        return self.ruta.exists()

    def crear(self, password: str, usuario: str = "admin") -> str:
        """Crea la cuenta. Devuelve el secreto TOTP para configurarlo en la app de 2FA."""
        prob = validar_politica_password(password)
        if prob:
            raise ValueError(" ".join(prob))
        if self.existe():
            raise FileExistsError("Ya existe un administrador.")
        salt = secrets.token_bytes(16)
        secreto = nuevo_secreto_totp()
        _escribir_privado(self.ruta, {"usuario": usuario, "salt": base64.b64encode(salt).decode(),
                                      "hash": _hash_pw(password, salt), "totp": secreto, "ultimo_contador": 0})
        return secreto

    def _datos(self) -> dict:
        return json.loads(self.ruta.read_text(encoding="utf-8"))

    @property
    def usuario(self) -> str:
        return self._datos()["usuario"]

    def cambiar_password(self, nueva: str):
        prob = validar_politica_password(nueva)
        if prob:
            raise ValueError(" ".join(prob))
        d = self._datos()
        salt = secrets.token_bytes(16)
        d["salt"], d["hash"] = base64.b64encode(salt).decode(), _hash_pw(nueva, salt)
        _escribir_privado(self.ruta, d)

    def nuevo_2fa(self) -> str:
        d = self._datos()
        d["totp"], d["ultimo_contador"] = nuevo_secreto_totp(), 0
        _escribir_privado(self.ruta, d)
        return d["totp"]

    # -- verificación
    def verificar_password(self, password: str) -> bool:
        d = self._datos()
        calc = _hash_pw(password, base64.b64decode(d["salt"]))
        return hmac.compare_digest(calc, d["hash"])

    def verificar_totp(self, codigo: str, ahora: float = None) -> bool:
        codigo = (codigo or "").strip().replace(" ", "")
        if not (codigo.isdigit() and len(codigo) == 6):
            return False
        d = self._datos()
        base = int((ahora or time.time()) // 30)
        for c in (base - 1, base, base + 1):
            if c > d.get("ultimo_contador", 0) and hmac.compare_digest(_codigo(d["totp"], c), codigo):
                d["ultimo_contador"] = c          # anti-reutilización del mismo código
                _escribir_privado(self.ruta, d)
                return True
        return False

    # -- límite de intentos (global: hay un único administrador)
    def _fallos(self, ahora: float):
        try:
            lista = json.loads(self.ruta_fallos.read_text())
        except (OSError, ValueError):
            lista = []
        return [t for t in lista if ahora - t < VENTANA_S]

    def segundos_bloqueo(self, ahora: float = None) -> int:
        ahora = ahora or time.time()
        f = self._fallos(ahora)
        if len(f) >= MAX_FALLOS:
            return max(0, int(f[-1] + BLOQUEO_S - ahora))
        return 0

    def registrar_fallo(self, ahora: float = None):
        ahora = ahora or time.time()
        f = self._fallos(ahora) + [ahora]
        _escribir_privado(self.ruta_fallos, f)  # type: ignore[arg-type]

    def limpiar_fallos(self):
        self.ruta_fallos.unlink(missing_ok=True)
