#!/usr/bin/env python3
"""Genera un EPUB 3 autocontenido a partir del curso en Markdown.

El conversor implementa únicamente el subconjunto de Markdown utilizado por
este libro, de modo que la generación no requiere dependencias externas.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import tempfile
import unicodedata
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path


IDENTIFICADOR = "urn:uuid:93af3348-9c6c-4fea-a2d6-curso-python-2026"
TITULO = "Python de cero a producción"
AUTOR = "Curso práctico"
IDIOMA = "es"


@dataclass(frozen=True)
class Capitulo:
    titulo: str
    slug: str
    markdown: str


def crear_slug(texto: str) -> str:
    normalizado = unicodedata.normalize("NFKD", texto)
    ascii_texto = normalizado.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_texto).strip("-")
    return slug or "capitulo"


def dividir_capitulos(markdown: str) -> list[Capitulo]:
    """Divide por encabezados H1 y preserva una introducción opcional."""
    capitulos: list[Capitulo] = []
    titulo_actual: str | None = None
    lineas_actuales: list[str] = []
    slugs_usados: set[str] = set()
    en_codigo = False

    def guardar() -> None:
        if titulo_actual is None:
            return
        base = crear_slug(titulo_actual)
        slug = base
        numero = 2
        while slug in slugs_usados:
            slug = f"{base}-{numero}"
            numero += 1
        slugs_usados.add(slug)
        capitulos.append(Capitulo(titulo_actual, slug, "\n".join(lineas_actuales)))

    for linea in markdown.splitlines():
        if linea.startswith("```"):
            en_codigo = not en_codigo
            if titulo_actual is not None:
                lineas_actuales.append(linea)
        elif linea.startswith("# ") and not en_codigo:
            guardar()
            titulo_actual = linea[2:].strip()
            lineas_actuales = []
        elif titulo_actual is not None:
            lineas_actuales.append(linea)
    guardar()

    if not capitulos:
        raise ValueError("El documento no contiene encabezados de nivel 1")
    return capitulos


def formato_inline(texto: str) -> str:
    """Escapa HTML y procesa código, énfasis y enlaces Markdown simples."""
    protegido: list[str] = []

    def guardar_codigo(coincidencia: re.Match[str]) -> str:
        protegido.append(f"<code>{html.escape(coincidencia.group(1))}</code>")
        return f"\x00{len(protegido) - 1}\x00"

    texto = re.sub(r"`([^`\n]+)`", guardar_codigo, texto)
    texto = html.escape(texto, quote=False)
    texto = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
        texto,
    )
    texto = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", texto)
    texto = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", texto)
    texto = re.sub(
        "\x00([0-9]+)\x00",
        lambda m: protegido[int(m.group(1))],
        texto,
    )
    return texto


def markdown_a_xhtml(markdown: str) -> str:
    """Convierte el subconjunto del curso a fragmentos XHTML válidos."""
    salida: list[str] = []
    parrafo: list[str] = []
    en_codigo = False
    codigo: list[str] = []
    lenguaje = ""
    tipo_lista: str | None = None

    def cerrar_parrafo() -> None:
        if parrafo:
            salida.append(f"<p>{formato_inline(' '.join(parrafo))}</p>")
            parrafo.clear()

    def cerrar_lista() -> None:
        nonlocal tipo_lista
        if tipo_lista:
            salida.append(f"</{tipo_lista}>")
            tipo_lista = None

    for linea in [*markdown.splitlines(), ""]:
        if en_codigo:
            if linea.startswith("```"):
                clase = f' class="language-{html.escape(lenguaje)}"' if lenguaje else ""
                salida.append(
                    f"<pre><code{clase}>{html.escape(chr(10).join(codigo))}</code></pre>"
                )
                en_codigo = False
                codigo = []
                lenguaje = ""
            else:
                codigo.append(linea)
            continue

        if linea.startswith("```"):
            cerrar_parrafo()
            cerrar_lista()
            en_codigo = True
            lenguaje = linea[3:].strip()
            continue

        encabezado = re.match(r"^(#{2,6})\s+(.+)$", linea)
        if encabezado:
            cerrar_parrafo()
            cerrar_lista()
            nivel = len(encabezado.group(1))
            texto = encabezado.group(2)
            salida.append(
                f'<h{nivel} id="{crear_slug(texto)}">{formato_inline(texto)}</h{nivel}>'
            )
            continue

        item = re.match(r"^\s*[-*]\s+(.+)$", linea)
        item_numerado = re.match(r"^\s*\d+\.\s+(.+)$", linea)
        if item or item_numerado:
            cerrar_parrafo()
            esperado = "ul" if item else "ol"
            if tipo_lista != esperado:
                cerrar_lista()
                tipo_lista = esperado
                salida.append(f"<{tipo_lista}>")
            contenido = (item or item_numerado).group(1)  # type: ignore[union-attr]
            salida.append(f"<li>{formato_inline(contenido)}</li>")
            continue

        if not linea.strip():
            cerrar_parrafo()
            cerrar_lista()
        else:
            cerrar_lista()
            parrafo.append(linea.strip())

    if en_codigo:
        raise ValueError("Bloque de código sin cerrar")
    return "\n".join(salida)


def documento_xhtml(titulo: str, cuerpo: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{IDIOMA}" lang="{IDIOMA}">
<head>
  <meta charset="UTF-8"/>
  <title>{html.escape(titulo)}</title>
  <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
  <main>
    <h1>{html.escape(titulo)}</h1>
    {cuerpo}
  </main>
</body>
</html>
"""


def portada_xhtml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{IDIOMA}" lang="{IDIOMA}">
<head>
  <meta charset="UTF-8"/>
  <title>Portada</title>
  <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body class="portada">
  <main>
    <p class="marca">CURSO PRÁCTICO</p>
    <h1>Python</h1>
    <h2>de cero a producción</h2>
    <p class="bajada">16 módulos · ejemplos · ejercicios · proyecto final</p>
    <p class="version">Python 3.12+ · Edición 2026</p>
  </main>
</body>
</html>
"""


ESTILOS = """
@namespace epub "http://www.idpf.org/2007/ops";
html { color: #17202a; background: #ffffff; }
body {
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.55;
  margin: 5%;
  max-width: 48rem;
}
h1, h2, h3, h4 {
  font-family: Arial, Helvetica, sans-serif;
  color: #173f5f;
  line-height: 1.2;
  page-break-after: avoid;
}
h1 { font-size: 2em; border-bottom: 0.15em solid #ffd43b; padding-bottom: 0.25em; }
h2 { margin-top: 1.8em; }
p, li { orphans: 3; widows: 3; }
li { margin-bottom: 0.35em; }
code { font-family: "DejaVu Sans Mono", Consolas, monospace; font-size: 0.9em; }
p code, li code { background: #eef3f6; padding: 0.08em 0.25em; border-radius: 0.2em; }
pre {
  background: #111b27;
  color: #f5f7fa;
  padding: 1em;
  border-left: 0.35em solid #3776ab;
  overflow-wrap: break-word;
  white-space: pre-wrap;
  page-break-inside: avoid;
}
a { color: #245c85; }
.portada { background: #173f5f; color: #ffffff; margin: 0; max-width: none; }
.portada main { padding: 18% 10%; text-align: center; }
.portada h1 { color: #ffd43b; border: 0; font-size: 4em; margin: 0; }
.portada h2 { color: #ffffff; font-size: 2em; margin: 0.2em 0 2em; }
.portada .marca { letter-spacing: 0.2em; }
.portada .bajada { font-size: 1.15em; }
.portada .version { margin-top: 5em; }
nav ol { list-style-type: none; padding-left: 0; }
nav li { margin: 0.65em 0; }
"""


CONTENEDOR = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


def crear_nav(capitulos: list[Capitulo]) -> str:
    enlaces = "\n".join(
        f'        <li><a href="{capitulo.slug}.xhtml">{html.escape(capitulo.titulo)}</a></li>'
        for capitulo in capitulos
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:epub="http://www.idpf.org/2007/ops"
      xml:lang="{IDIOMA}" lang="{IDIOMA}">
<head>
  <meta charset="UTF-8"/>
  <title>Índice</title>
  <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Índice</h1>
    <ol>
      <li><a href="cover.xhtml">Portada</a></li>
{enlaces}
    </ol>
  </nav>
</body>
</html>
"""


def crear_opf(capitulos: list[Capitulo], modificado: str) -> str:
    manifiesto = "\n".join(
        f'    <item id="c{indice}" href="{capitulo.slug}.xhtml" media-type="application/xhtml+xml"/>'
        for indice, capitulo in enumerate(capitulos, start=1)
    )
    lomo = "\n".join(
        f'    <itemref idref="c{indice}"/>'
        for indice in range(1, len(capitulos) + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0"
         unique-identifier="book-id" xml:lang="{IDIOMA}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">{IDENTIFICADOR}</dc:identifier>
    <dc:title>{TITULO}</dc:title>
    <dc:language>{IDIOMA}</dc:language>
    <dc:creator>{AUTOR}</dc:creator>
    <dc:description>Curso práctico de Python en 16 módulos, desde fundamentos hasta APIs, calidad y Docker.</dc:description>
    <dc:subject>Python</dc:subject>
    <dc:subject>Programación</dc:subject>
    <meta property="dcterms:modified">{modificado}T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>
    <item id="css" href="style.css" media-type="text/css"/>
{manifiesto}
  </manifest>
  <spine>
    <itemref idref="cover"/>
{lomo}
  </spine>
</package>
"""


def escribir_texto(ruta: Path, contenido: str) -> None:
    ruta.write_text(contenido, encoding="utf-8", newline="\n")


def construir_epub(origen: Path, destino: Path) -> None:
    markdown = origen.read_text(encoding="utf-8")
    capitulos = dividir_capitulos(markdown)

    with tempfile.TemporaryDirectory(prefix="curso-python-") as temporal:
        raiz = Path(temporal)
        meta_inf = raiz / "META-INF"
        oebps = raiz / "OEBPS"
        meta_inf.mkdir()
        oebps.mkdir()

        escribir_texto(raiz / "mimetype", "application/epub+zip")
        escribir_texto(meta_inf / "container.xml", CONTENEDOR)
        escribir_texto(oebps / "style.css", ESTILOS.strip() + "\n")
        escribir_texto(oebps / "cover.xhtml", portada_xhtml())
        escribir_texto(oebps / "nav.xhtml", crear_nav(capitulos))
        escribir_texto(oebps / "content.opf", crear_opf(capitulos, date.today().isoformat()))

        for capitulo in capitulos:
            cuerpo = markdown_a_xhtml(capitulo.markdown)
            escribir_texto(
                oebps / f"{capitulo.slug}.xhtml",
                documento_xhtml(capitulo.titulo, cuerpo),
            )

        destino.parent.mkdir(parents=True, exist_ok=True)
        temporal_epub = destino.with_suffix(".tmp")
        with zipfile.ZipFile(temporal_epub, "w") as archivo:
            archivo.write(
                raiz / "mimetype",
                "mimetype",
                compress_type=zipfile.ZIP_STORED,
            )
            for ruta in sorted(raiz.rglob("*")):
                if ruta.is_file() and ruta.name != "mimetype":
                    archivo.write(
                        ruta,
                        ruta.relative_to(raiz).as_posix(),
                        compress_type=zipfile.ZIP_DEFLATED,
                        compresslevel=9,
                    )
        temporal_epub.replace(destino)

    digest = hashlib.sha256(destino.read_bytes()).hexdigest()
    print(f"Generado: {destino} ({destino.stat().st_size:,} bytes)")
    print(f"SHA-256: {digest}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera el curso en formato EPUB 3")
    parser.add_argument(
        "--origen",
        type=Path,
        default=Path(__file__).with_name("curso-python.md"),
    )
    parser.add_argument(
        "--destino",
        type=Path,
        default=Path(__file__).parent.parent / "dist" / "curso-python.epub",
    )
    argumentos = parser.parse_args()
    construir_epub(argumentos.origen.resolve(), argumentos.destino.resolve())


if __name__ == "__main__":
    main()
