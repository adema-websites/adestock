"""Panel web local (Flask). Solo escucha en 127.0.0.1; ningún endpoint es público."""
import hmac
import re
import secrets
import shutil
import time

from flask import (Flask, Response, abort, flash, g, redirect, render_template, request, send_file,
                   session, url_for)

from . import auditoria as A
from . import config as C
from . import firma as F
from . import publicador as P
from .auth import Credenciales
from .config import Entorno
from .validador import FORMATOS

IDLE_S = 30 * 60
ABS_S = 8 * 3600
STAGING_S = 3600
RE_TOKEN = re.compile(r"^[A-Za-z0-9_-]{16,32}$")
RE_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def crear_app(env: Entorno, puerto: int = 8765, https: bool = False) -> Flask:
    app = Flask(__name__)
    env.estado.mkdir(parents=True, exist_ok=True)
    ruta_key = env.estado / "secret_key"
    if not ruta_key.exists():
        ruta_key.write_bytes(secrets.token_bytes(32))
    app.secret_key = ruta_key.read_bytes()
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Strict",
                      SESSION_COOKIE_SECURE=https, SESSION_COOKIE_NAME="adestock_temas",
                      MAX_CONTENT_LENGTH=24 * 1024 * 1024)
    cred = Credenciales(env.estado)
    sesiones: dict = {}
    hosts = {f"127.0.0.1:{puerto}", f"localhost:{puerto}", "localhost", "127.0.0.1"}

    def ahora():
        return time.time()

    def audit(evento, **datos):
        usuario = cred.usuario if cred.existe() else "-"
        A.registrar(env.auditoria, evento, usuario=usuario, ip=request.remote_addr or "-", **datos)

    def sesion_actual(crear=False):
        sid = session.get("sid")
        s = sesiones.get(sid)
        if s and (ahora() - s["last"] > IDLE_S or ahora() - s["iat"] > ABS_S):
            sesiones.pop(sid, None)
            s = None
        if s is None and crear:
            sid = secrets.token_urlsafe(24)
            s = {"auth": False, "csrf": secrets.token_urlsafe(24), "iat": ahora(), "last": ahora()}
            sesiones[sid] = s
            session.clear()
            session["sid"] = sid
        if s:
            s["last"] = ahora()
        return s

    @app.before_request
    def _guardia():
        if request.host not in hosts:           # anti DNS-rebinding
            abort(400)
        g.s = sesion_actual()
        if request.endpoint == "static":
            return
        if request.method == "POST":
            origen = request.headers.get("Origin")
            if origen and origen.split("://", 1)[-1] not in hosts:
                abort(403)
            # Sin sesión: se corta antes de mirar el CSRF (no hay nada que proteger ni que crear).
            if not (g.s and g.s["auth"]) and request.endpoint != "login":
                audit("acceso_sin_sesion", ruta=request.path)
                return Response("No autenticado.", 401)
            tok = request.form.get("csrf", "")
            if not g.s or not hmac.compare_digest(tok, g.s["csrf"]):
                audit("csrf_rechazado", ruta=request.path)
                abort(403)
        if request.endpoint != "login" and not (g.s and g.s["auth"]):
            return redirect(url_for("login"))

    @app.after_request
    def _cabeceras(r):
        r.headers["Content-Security-Policy"] = ("default-src 'none'; style-src 'self'; img-src 'self'; "
                                                "form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
        r.headers["X-Content-Type-Options"] = "nosniff"
        r.headers["X-Frame-Options"] = "DENY"
        r.headers["Referrer-Policy"] = "no-referrer"
        r.headers["Cache-Control"] = "no-store"
        return r

    @app.context_processor
    def _ctx():
        s = getattr(g, "s", None) or {}
        return {"csrf": s.get("csrf", ""), "autenticado": bool(s.get("auth")), "FORMATOS": FORMATOS}

    def exigir_password(pw: str) -> bool:
        """Re-autenticación para acciones que firman. Cuenta para el límite de intentos."""
        if cred.segundos_bloqueo():
            return False
        if cred.verificar_password(pw):
            return True
        cred.registrar_fallo()
        audit("password_incorrecto_accion", ruta=request.path)
        return False

    # ------------------------------------------------------------ login
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            sesion_actual(crear=True)
            return render_template("login.html", csrf=session_csrf())
        bloqueo = cred.segundos_bloqueo()
        if bloqueo:
            audit("login_bloqueado", segundos=bloqueo)
            flash(f"Demasiados intentos. Probá de nuevo en {bloqueo // 60 + 1} min.")
            return render_template("login.html", csrf=session_csrf()), 429
        ok = cred.existe() and cred.verificar_password(request.form.get("password", "")) \
            and cred.verificar_totp(request.form.get("codigo", ""))
        if not ok:
            cred.registrar_fallo()
            audit("login_fallido")
            flash("Credenciales o código incorrectos.")
            return render_template("login.html", csrf=session_csrf()), 401
        cred.limpiar_fallos()
        sesiones.pop(session.get("sid"), None)      # rotación de sesión (anti fijación)
        session.clear()
        sid = secrets.token_urlsafe(24)
        sesiones[sid] = {"auth": True, "csrf": secrets.token_urlsafe(24), "iat": ahora(), "last": ahora()}
        session["sid"] = sid
        audit("login_ok")
        return redirect(url_for("inicio"))

    def session_csrf():
        return sesion_actual(crear=True)["csrf"]

    @app.post("/logout")
    def logout():
        audit("logout")
        sesiones.pop(session.get("sid"), None)
        session.clear()
        return redirect(url_for("login"))

    # ------------------------------------------------------------ inicio
    @app.get("/")
    def inicio():
        cat = P.cargar_catalogo(env)
        temas = []
        for tid, t in sorted(cat["temas"].items()):
            v = P.ultima_version(t)
            temas.append({"id": tid, "nombre": v["nombre"], "version": v["version"],
                          "retirado": t.get("retirado"), "premium": t.get("premium"),
                          "n": len(t["versiones"]), "sha256": v["sha256"]})
        return render_template("index.html", temas=temas, cadena_ok=A.verificar_cadena(env.auditoria))

    # ------------------------------------------------------------ subir
    def limpiar_staging():
        base = env.estado / "staging"
        if base.exists():
            for d in base.iterdir():
                if ahora() - d.stat().st_mtime > STAGING_S:
                    shutil.rmtree(d, ignore_errors=True)

    @app.route("/subir", methods=["GET", "POST"])
    def subir():
        if request.method == "GET":
            return render_template("subir.html", errores=[], form={})
        limpiar_staging()
        f_zip = request.files.get("zip")
        zip_bytes = f_zip.read(C.ZIP_MAX_BYTES + 1) if f_zip else b""
        f_min = request.files.get("miniatura")
        miniatura = f_min.read(C.MINIATURA_MAX_BYTES + 1) if f_min and f_min.filename else None
        capturas = [f.read(C.CAPTURA_MAX_BYTES + 1) for f in request.files.getlist("capturas")
                    if f and f.filename]
        etiquetas = [t.strip().lower() for t in request.form.get("etiquetas", "").split(",") if t.strip()]
        formatos = request.form.getlist("formatos")
        premium = request.form.get("premium") == "on"
        if not zip_bytes:
            return render_template("subir.html", errores=["Falta el archivo ZIP."], form=request.form), 400
        prep = P.preparar(env, zip_bytes, miniatura, capturas, etiquetas, formatos, premium)
        audit("subida_validada" if prep.ok else "subida_rechazada",
              archivo=(f_zip.filename or "")[:80], sha256=prep.resultado.sha256, bytes=len(zip_bytes),
              errores=prep.errores[:10])
        if not prep.ok:
            return render_template("subir.html", errores=prep.errores, form=request.form), 422
        token = secrets.token_urlsafe(16)
        d = env.estado / "staging" / token
        d.mkdir(parents=True)
        (d / "tema.zip").write_bytes(zip_bytes)
        if miniatura:
            (d / "miniatura.webp").write_bytes(miniatura)
        for i, c in enumerate(capturas, 1):
            (d / f"vista-{i}.webp").write_bytes(c)
        (d / "meta.txt").write_text("\n".join([",".join(etiquetas), ",".join(formatos),
                                                "1" if premium else "0"]))
        return redirect(url_for("confirmar", token=token))

    def cargar_staging(token):
        if not RE_TOKEN.match(token):
            abort(404)
        d = env.estado / "staging" / token
        if not d.is_dir() or ahora() - d.stat().st_mtime > STAGING_S:
            abort(404)
        et, fo, pr = (d / "meta.txt").read_text().split("\n")
        mini = (d / "miniatura.webp").read_bytes() if (d / "miniatura.webp").exists() else None
        caps = [p.read_bytes() for p in sorted(d.glob("vista-*.webp"))]
        prep = P.preparar(env, (d / "tema.zip").read_bytes(), mini, caps,
                          [x for x in et.split(",") if x], [x for x in fo.split(",") if x], pr == "1")
        return d, prep

    @app.get("/confirmar/<token>")
    def confirmar(token):
        d, prep = cargar_staging(token)
        return render_template("confirmar.html", p=prep, token=token,
                               tiene_mini=(d / "miniatura.webp").exists())

    @app.get("/preview/<token>/miniatura")
    def preview(token):
        if not RE_TOKEN.match(token):
            abort(404)
        ruta = env.estado / "staging" / token / "miniatura.webp"
        if not ruta.exists():
            abort(404)
        return send_file(ruta, mimetype="image/webp")

    @app.post("/publicar/<token>")
    def publicar(token):
        d, prep = cargar_staging(token)
        if not prep.ok:
            return render_template("confirmar.html", p=prep, token=token, tiene_mini=False), 422
        if not exigir_password(request.form.get("password", "")):
            flash("Contraseña incorrecta o panel bloqueado.")
            return redirect(url_for("confirmar", token=token))
        try:
            priv = F.cargar_privada(env.estado, request.form["password"])
            P.publicar(env, prep, priv)
        except (P.PublicacionError, ValueError, FileExistsError) as exc:
            audit("publicacion_fallida", tema=prep.tema_id, version=prep.version, motivo=str(exc))
            flash(f"No se pudo publicar: {exc}")
            return redirect(url_for("confirmar", token=token))
        audit("publicado", tema=prep.tema_id, version=prep.version, sha256=prep.resultado.sha256,
              bytes=prep.resultado.bytes, premium=prep.premium)
        shutil.rmtree(d, ignore_errors=True)
        return render_template("publicado.html", p=prep)

    # ------------------------------------------------------------ editar / retirar
    @app.route("/tema/<tid>", methods=["GET", "POST"])
    def tema(tid):
        if not RE_ID.match(tid):
            abort(404)
        cat = P.cargar_catalogo(env)
        ent = cat["temas"].get(tid)
        if not ent:
            abort(404)
        if request.method == "POST":
            accion = request.form.get("accion")
            if not exigir_password(request.form.get("password", "")):
                flash("Contraseña incorrecta o panel bloqueado.")
                return redirect(url_for("tema", tid=tid))
            try:
                priv = F.cargar_privada(env.estado, request.form["password"])
                if accion == "meta":
                    et = [t.strip().lower() for t in request.form.get("etiquetas", "").split(",") if t.strip()]
                    pr = request.form.get("premium") == "on"
                    P.editar_meta(env, tid, et, request.form.getlist("formatos"), pr, priv)
                    audit("meta_editada", tema=tid, premium=pr, etiquetas=et)
                elif accion in ("retirar", "restaurar"):
                    P.cambiar_retiro(env, tid, accion == "retirar", priv)
                    audit(accion, tema=tid)
                else:
                    abort(400)
                flash("Listo: índice regenerado y firmado. Falta hacer commit y push.")
            except (P.PublicacionError, ValueError) as exc:
                flash(f"No se pudo: {exc}")
            return redirect(url_for("tema", tid=tid))
        return render_template("tema.html", tid=tid, t=ent, v=P.ultima_version(ent))

    # ------------------------------------------------------------ mantenimiento
    @app.route("/verificar", methods=["GET", "POST"])
    def verificar():
        problemas = None
        if request.method == "POST":
            ruta_pub = env.estado / "clave_publica.txt"
            pub = ruta_pub.read_text().strip() if ruta_pub.exists() else None
            problemas = P.verificar_publicacion(env, pub)
            audit("verificacion", problemas=len(problemas))
        return render_template("verificar.html", problemas=problemas)

    @app.post("/backup")
    def backup():
        ruta = P.hacer_backup(env)
        audit("backup", archivo=ruta.name)
        flash(f"Backup creado: {ruta}")
        return redirect(url_for("inicio"))

    @app.get("/auditoria")
    def auditoria():
        return render_template("auditoria.html", filas=A.leer(env.auditoria),
                               cadena_ok=A.verificar_cadena(env.auditoria))

    return app
