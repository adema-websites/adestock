"""CLI: python -m adestock_temas <comando>   (ejecutar desde la carpeta admin-temas)."""
import argparse
import getpass
import os
import sys
from pathlib import Path

from . import auditoria as A
from . import firma as F
from . import publicador as P
from .auth import Credenciales, uri_totp, validar_politica_password
from .config import Entorno


def _pedir_password(nuevo=False, etiqueta="Contraseña"):
    env_pw = os.environ.get("ADESTOCK_TEMAS_PASSWORD")   # solo para automatización/pruebas
    if env_pw:
        return env_pw
    pw = getpass.getpass(f"{etiqueta}: ")
    if nuevo:
        if getpass.getpass("Repetila: ") != pw:
            sys.exit("No coinciden.")
    return pw


def _audit(env, evento, **datos):
    A.registrar(env.auditoria, evento, usuario="admin", ip="cli", **datos)


def cmd_init(env, a):
    cred = Credenciales(env.estado)
    if cred.existe() or F.existe_clave(env.estado):
        sys.exit("Ya está inicializado. Para cambios usá cambiar-password / nuevo-2fa / rotar-clave.")
    pw = _pedir_password(nuevo=True, etiqueta="Elegí una contraseña (≥14, 3 tipos de caracteres)")
    prob = validar_politica_password(pw)
    if prob:
        sys.exit("Contraseña débil: " + " ".join(prob))
    secreto = cred.crear(pw)
    pub = F.generar_clave(env.estado, pw)
    _audit(env, "init")
    print("\n== 2FA (TOTP) ==\nCargá este secreto en tu app (Google Authenticator, Aegis, 1Password…):")
    print("  secreto:", secreto)
    print("  URI    :", uri_totp(secreto))
    print("\n== Clave pública de firma Ed25519 (base64, incrustar en el sistema Adestock) ==\n ", pub)
    print(f"\nEstado (secretos, NO subir a git): {env.estado}")


def cmd_panel(env, a):
    from .web import crear_app
    if not Credenciales(env.estado).existe():
        sys.exit("Primero ejecutá: python -m adestock_temas init")
    app = crear_app(env, puerto=a.puerto, https=False)
    print(f"Panel en http://127.0.0.1:{a.puerto}  (solo local; Ctrl+C para cerrar)")
    app.run(host="127.0.0.1", port=a.puerto, debug=False, use_reloader=False)


def cmd_publicar(env, a):
    cred = Credenciales(env.estado)
    pw = _pedir_password()
    if cred.segundos_bloqueo() or not cred.verificar_password(pw):
        cred.registrar_fallo()
        sys.exit("Contraseña incorrecta o bloqueado por intentos.")
    leer = lambda p: Path(p).read_bytes() if p else None  # noqa: E731
    et = [t.strip().lower() for t in (a.etiquetas or "").split(",") if t.strip()]
    prep = P.preparar(env, leer(a.zip), leer(a.miniatura), [leer(c) for c in (a.captura or [])], et,
                      a.formatos.split(","), a.premium)
    if not prep.ok:
        _audit(env, "subida_rechazada_cli", archivo=Path(a.zip).name, sha256=prep.resultado.sha256,
               errores=prep.errores[:10])
        sys.exit("RECHAZADO:\n - " + "\n - ".join(prep.errores))
    priv = F.cargar_privada(env.estado, pw)
    P.publicar(env, prep, priv)
    _audit(env, "publicado", tema=prep.tema_id, version=prep.version, sha256=prep.resultado.sha256,
           bytes=prep.resultado.bytes, premium=prep.premium, archivo=Path(a.zip).name)
    print(f"Publicado {prep.tema_id} {prep.version}\n  bytes : {prep.resultado.bytes}\n  sha256: {prep.resultado.sha256}")


def cmd_republicar(env, a):
    pw = _pedir_password()
    cred = Credenciales(env.estado)
    if not cred.verificar_password(pw):
        sys.exit("Contraseña incorrecta.")
    priv = F.cargar_privada(env.estado, pw)
    P.snapshot(env, "republicar")
    P.regenerar_indice(env, P.cargar_catalogo(env), priv)
    _audit(env, "indice_republicado")
    print("index.json e index.json.sig regenerados.")


def cmd_verificar(env, a):
    ruta = env.estado / "clave_publica.txt"
    pub = a.clave or (ruta.read_text().strip() if ruta.exists() else None)
    problemas = P.verificar_publicacion(env, pub)
    if problemas:
        sys.exit("PROBLEMAS:\n - " + "\n - ".join(problemas))
    print("OK: sha256, tamaños, contenido de los ZIP y firma verificados.")


def cmd_backup(env, a):
    ruta = P.hacer_backup(env, Path(a.destino) if a.destino else None)
    _audit(env, "backup", archivo=ruta.name)
    print("Backup:", ruta)


def cmd_clave_publica(env, a):
    ruta = env.estado / "clave_publica.txt"
    pub = ruta.read_text().strip()
    print(pub)
    if a.pem:
        print(F.publica_pem(pub))


def cmd_rotar(env, a):
    pw = _pedir_password()
    if not Credenciales(env.estado).verificar_password(pw):
        sys.exit("Contraseña incorrecta.")
    F.cargar_privada(env.estado, pw)  # comprueba que abre la actual
    pub = F.rotar(env.estado, pw)
    priv = F.cargar_privada(env.estado, pw)
    P.regenerar_indice(env, P.cargar_catalogo(env), priv)
    _audit(env, "clave_rotada", nueva_publica=pub)
    print("Nueva clave pública:", pub, "\nÍndice re-firmado. La anterior quedó en claves-anteriores/.")


def cmd_cambiar_password(env, a):
    cred = Credenciales(env.estado)
    vieja = _pedir_password(etiqueta="Contraseña actual")
    if not cred.verificar_password(vieja):
        sys.exit("Contraseña incorrecta.")
    os.environ.pop("ADESTOCK_TEMAS_PASSWORD", None)
    nueva = _pedir_password(nuevo=True, etiqueta="Nueva contraseña")
    cred.cambiar_password(nueva)
    F.recifrar(env.estado, vieja, nueva)
    _audit(env, "password_cambiada")
    print("Listo.")


def cmd_nuevo_2fa(env, a):
    cred = Credenciales(env.estado)
    if not cred.verificar_password(_pedir_password()):
        sys.exit("Contraseña incorrecta.")
    secreto = cred.nuevo_2fa()
    _audit(env, "2fa_regenerado")
    print("Nuevo secreto:", secreto, "\nURI:", uri_totp(secreto))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="adestock_temas")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(f=cmd_init)
    p = sub.add_parser("panel")
    p.add_argument("--puerto", type=int, default=8765)
    p.set_defaults(f=cmd_panel)
    p = sub.add_parser("publicar")
    p.add_argument("zip")
    p.add_argument("--miniatura")
    p.add_argument("--captura", action="append")
    p.add_argument("--etiquetas", default="")
    p.add_argument("--formatos", default="a4,a4h,post,postv,historia")
    p.add_argument("--premium", action="store_true")
    p.set_defaults(f=cmd_publicar)
    sub.add_parser("republicar-indice").set_defaults(f=cmd_republicar)
    p = sub.add_parser("verificar")
    p.add_argument("--clave", help="clave pública base64 (por defecto, la del estado)")
    p.set_defaults(f=cmd_verificar)
    p = sub.add_parser("backup")
    p.add_argument("--destino")
    p.set_defaults(f=cmd_backup)
    p = sub.add_parser("clave-publica")
    p.add_argument("--pem", action="store_true")
    p.set_defaults(f=cmd_clave_publica)
    sub.add_parser("rotar-clave").set_defaults(f=cmd_rotar)
    sub.add_parser("cambiar-password").set_defaults(f=cmd_cambiar_password)
    sub.add_parser("nuevo-2fa").set_defaults(f=cmd_nuevo_2fa)
    a = ap.parse_args(argv)
    a.f(Entorno.desde_env(), a)


if __name__ == "__main__":
    main()
