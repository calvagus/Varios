# Curso de Python

Material en español para aprender Python desde los fundamentos hasta APIs,
calidad de código y Docker.

El libro listo para descargar está en
[`dist/curso-python.epub`](dist/curso-python.epub).

## Regenerar el EPUB

Solo requiere Python 3.12 o superior:

```bash
python curso-python/generar_epub.py
```

El contenido fuente se encuentra en
[`curso-python/curso-python.md`](curso-python/curso-python.md). El generador crea
un EPUB 3 autocontenido sin dependencias externas.
