"""Fase 0: inventario de URLs del sitio estatico actual.

Uso (desde la raiz del repo):  python scripts/inventario_fase0.py
Genera docs/inventario-urls.csv, docs/inventario-enlaces-rotos.csv y docs/inventario-activos.csv.
Solo lee; no modifica el sitio.
"""
import csv, json, re, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, urldefrag, unquote

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
SITE = "https://adestock.com.ar"
SKIP_DIRS = {".git", "admin-temas", "node_modules", "docs", "scripts"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self._t = False
        self.meta = {}; self.canonical = ""; self.links = []; self.h1 = 0
        self.jsonld = []; self._j = False; self._buf = ""
        self.scripts = []; self.imgs = []; self.hreflang = []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "title": self._t = True
        elif tag == "meta":
            k = a.get("name") or a.get("property")
            if k: self.meta[k.lower()] = a.get("content", "")
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            if rel == "canonical": self.canonical = a.get("href", "")
            if rel == "alternate" and a.get("hreflang"): self.hreflang.append(a["hreflang"])
        elif tag == "a" and a.get("href"): self.links.append(a["href"])
        elif tag == "h1": self.h1 += 1
        elif tag == "script":
            if a.get("type") == "application/ld+json": self._j = True; self._buf = ""
            elif a.get("src"): self.scripts.append(a["src"])
        elif tag == "img" and a.get("src"): self.imgs.append(a["src"])

    def handle_endtag(self, tag):
        if tag == "title": self._t = False
        if tag == "script" and self._j:
            self._j = False
            try:
                d = json.loads(self._buf)
                for n in (d if isinstance(d, list) else d.get("@graph", [d])):
                    t = n.get("@type"); self.jsonld.append("/".join(t) if isinstance(t, list) else str(t))
            except Exception:
                self.jsonld.append("JSON-INVALIDO")

    def handle_data(self, d):
        if self._t: self.title += d
        if self._j: self._buf += d


def url_of(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[: -len("index.html")]
    return "/" + rel


def resolve(href: str, page_url: str):
    """Devuelve ruta de archivo local si el enlace es interno, None si es externo/ignorable."""
    href, _ = urldefrag(href.strip())
    if not href or re.match(r"^(mailto:|tel:|javascript:|data:|#)", href): return None
    p = urlparse(href)
    if p.scheme in ("http", "https"):
        if p.netloc not in ("adestock.com.ar", "www.adestock.com.ar"): return None
        path = p.path
    elif p.scheme: return None
    else:
        base = page_url if page_url.endswith("/") else page_url.rsplit("/", 1)[0] + "/"
        path = href.split("?")[0] if href.startswith("/") else base + href.split("?")[0]
    segs = []
    for s in unquote(path).split("/"):
        if s == "..": segs and segs.pop()
        elif s not in ("", "."): segs.append(s)
    return "/".join(segs) + ("/" if path.endswith("/") else "")


def exists(rel: str) -> bool:
    if rel in ("", "/"): return (ROOT / "index.html").exists()
    p = ROOT / rel
    return p.is_file() or (p.is_dir() and (p / "index.html").exists())


def main():
    OUT.mkdir(exist_ok=True)
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8") if (ROOT / "sitemap.xml").exists() else ""
    in_sitemap = set(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap))
    pages = []
    for f in sorted(ROOT.rglob("*.html")):
        if SKIP_DIRS & set(f.relative_to(ROOT).parts[:-1]): continue
        pages.append(f)

    rows, broken, inbound = [], [], {}
    for f in pages:
        u = url_of(f); pg = Page(); pg.feed(f.read_text(encoding="utf-8", errors="replace"))
        for l in pg.links:
            r = resolve(l, u)
            if r is None: continue
            if not exists(r): broken.append((u, l))
            else: inbound[r] = inbound.get(r, 0) + 1
        canon = pg.canonical
        rows.append({
            "url": u, "archivo": f.relative_to(ROOT).as_posix(),
            "title": pg.title.strip(), "title_len": len(pg.title.strip()),
            "description_len": len(pg.meta.get("description", "")),
            "canonical": canon,
            "canonical_ok": "si" if canon == SITE + u else "REVISAR",
            "robots": pg.meta.get("robots", ""),
            "h1": pg.h1, "og_title": "si" if "og:title" in pg.meta else "NO",
            "og_image": "si" if "og:image" in pg.meta else "NO",
            "twitter_card": "si" if "twitter:card" in pg.meta else "NO",
            "jsonld": " | ".join(pg.jsonld), "hreflang": ",".join(pg.hreflang),
            "en_sitemap": "si" if SITE + u in in_sitemap else "no",
            "enlaces_internos": sum(1 for l in pg.links if resolve(l, u) is not None),
            "scripts": " ".join(pg.scripts),
        })
    for r in rows:
        r["enlaces_entrantes"] = inbound.get(r["url"].lstrip("/"), 0)

    with open(OUT / "inventario-urls.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(OUT / "inventario-enlaces-rotos.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh); w.writerow(["pagina", "enlace"]); w.writerows(sorted(set(broken)))

    # sitemap -> existe?
    orphan = [u for u in in_sitemap if not exists(urlparse(u).path.lstrip("/"))]

    # activos pesados
    assets = []
    for f in ROOT.rglob("*"):
        if f.is_file() and not (SKIP_DIRS & set(f.relative_to(ROOT).parts)) and f.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".mp4", ".zip", ".js", ".css", ".json"}:
            assets.append((f.stat().st_size, f.relative_to(ROOT).as_posix()))
    assets.sort(reverse=True)
    with open(OUT / "inventario-activos.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh); w.writerow(["bytes", "ruta"]); w.writerows(assets)

    print(f"paginas HTML publicas: {len(rows)}")
    print(f"en sitemap: {sum(r['en_sitemap']=='si' for r in rows)} | sitemap apunta a inexistentes: {orphan}")
    print(f"canonical a revisar: {[r['url'] for r in rows if r['canonical_ok']!='si']}")
    print(f"sin og:image: {[r['url'] for r in rows if r['og_image']=='NO']}")
    print(f"h1 != 1: {[(r['url'], r['h1']) for r in rows if r['h1']!=1]}")
    print(f"noindex: {[r['url'] for r in rows if 'noindex' in r['robots']]}")
    print(f"enlaces internos rotos: {len(set(broken))}")
    print("top activos:"); [print(f"  {s/1024:.0f} KiB  {p}") for s, p in assets[:8]]


if __name__ == "__main__":
    sys.exit(main())
