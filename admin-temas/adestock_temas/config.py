"""Rutas y límites del contrato (README_WEB_TIENDA_TEMAS_REVISTAS.md)."""
import os
from dataclasses import dataclass
from pathlib import Path

ADMIN_DIR = Path(__file__).resolve().parent.parent

# --- Límites del contrato (sección 3.4, 3.3, 2.1) ---
ZIP_MAX_BYTES = 8 * 1024 * 1024
ZIP_MAX_ARCHIVOS = 20
ZIP_MAX_DESCOMPRIMIDO = 16 * 1024 * 1024   # tope anti ZIP bomba (suma real descomprimida)
CSS_MAX_BYTES = 50_000
FONDO_MAX_BYTES = 5 * 1024 * 1024
JSON_MAX_BYTES = 64 * 1024
VISTA_PREVIA_MAX_BYTES = 2 * 1024 * 1024
INSTRUCCIONES_MAX_BYTES = 200 * 1024
MINIATURA_MAX_BYTES = 150 * 1024
CAPTURA_MAX_BYTES = 400 * 1024
CAPTURAS_MAX = 4
IMAGEN_MAX_PIXELES = 40_000_000
RATIO_SOSPECHOSO = 200            # descomprimido/comprimido
FORMATO_ACTUAL = 1


@dataclass
class Entorno:
    sitio: Path        # raíz del sitio estático (repo)
    estado: Path       # secretos, sesión, auditoría, backups: FUERA del repo
    catalogo: Path     # catálogo (fuente de verdad del índice)

    @property
    def api(self) -> Path:
        return self.sitio / "api" / "temas-revista"

    @property
    def auditoria(self) -> Path:
        return self.estado / "auditoria.jsonl"

    @classmethod
    def desde_env(cls) -> "Entorno":
        sitio = Path(os.environ.get("ADESTOCK_SITIO") or ADMIN_DIR.parent)
        if os.environ.get("ADESTOCK_TEMAS_ESTADO"):
            estado = Path(os.environ["ADESTOCK_TEMAS_ESTADO"])
        elif os.name == "nt":
            estado = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "adestock-temas-admin"
        else:
            estado = Path.home() / ".adestock-temas-admin"
        catalogo = Path(os.environ.get("ADESTOCK_CATALOGO") or ADMIN_DIR / "catalogo.json")
        return cls(sitio=sitio, estado=estado, catalogo=catalogo)
