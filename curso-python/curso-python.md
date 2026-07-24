# Python de cero a producción

## Un curso práctico en 16 módulos

**Edición 2026 · Python 3.12+**

Este libro propone un recorrido desde tu primera variable hasta una API contenida con Docker. No hace falta experiencia previa: sí necesitás curiosidad, una computadora y tiempo para escribir código. La lectura sola no alcanza. Copiá los ejemplos, cambialos, rompé algo a propósito y explicá con tus palabras por qué funciona.

### Cómo usar este curso

Cada módulo contiene objetivos, conceptos, un ejemplo guiado, práctica y un desafío. La práctica transversal es **Bitácora**, una aplicación de tareas que crece con vos: primero será una lista, luego un paquete probado, una API y finalmente un contenedor.

Convenciones:

- Los comandos que comienzan con `$` se ejecutan en una terminal; no escribas el signo `$`.
- El código usa cuatro espacios para indentar.
- Los nombres de variables y funciones están en castellano para favorecer la lectura; en equipos internacionales suele usarse inglés.
- Buscá entender los mensajes de error antes de corregirlos.

Para comprobar tu instalación:

```bash
python --version
python -c "print('¡Hola, Python!')"
```

En algunos sistemas el comando es `python3`. Creá una carpeta para el curso y guardá allí cada ejercicio. La documentación oficial en `docs.python.org/es/3/` será tu referencia permanente.

### Ruta de aprendizaje

Al terminar, vas a poder modelar problemas con Python, organizar proyectos, automatizar archivos, probar código, usar concurrencia, colaborar con Git, construir una API con FastAPI y distribuirla en un contenedor. El objetivo no es memorizar toda la sintaxis: es aprender a dividir problemas, buscar documentación y verificar resultados.

# Módulo 01 · Variables, tipos y estructuras básicas

## Objetivos

- Declarar variables con nombres claros.
- Operar con enteros, flotantes, cadenas y booleanos.
- Tomar decisiones con condicionales.
- Agrupar información con tuplas, conjuntos y diccionarios.

## Los valores y sus nombres

Una variable vincula un nombre con un objeto. Python infiere el tipo en tiempo de ejecución:

```python
nombre = "Ada"
edad = 36
altura = 1.65
programa = True

print(type(nombre), type(edad), type(altura), type(programa))
```

Usá nombres descriptivos en `snake_case`. Python distingue mayúsculas: `precio` y `Precio` son nombres diferentes. Las constantes se escriben por convención en mayúsculas, por ejemplo `IVA = 0.21`.

Los números admiten `+`, `-`, `*`, `/`, división entera `//`, resto `%` y potencia `**`. Cuidado con los flotantes: se representan en binario y `0.1 + 0.2` no es exactamente `0.3`. Para dinero real se suele utilizar `decimal.Decimal`.

```python
precio = 1250.0
cantidad = 3
subtotal = precio * cantidad
total = subtotal * (1 + 0.21)
print(f"Total: ${total:,.2f}")
```

Las cadenas son inmutables. Podés indexarlas, cortarlas y aplicar métodos que devuelven otra cadena:

```python
mensaje = "  aprender Python  "
limpio = mensaje.strip().title()
print(limpio)
print(limpio[:8])
```

Los booleanos `True` y `False` aparecen al comparar: `==`, `!=`, `<`, `<=`, `>` y `>=`. Se combinan con `and`, `or` y `not`.

```python
edad = 19
tiene_entrada = True
if edad >= 18 and tiene_entrada:
    print("Puede ingresar")
else:
    print("No puede ingresar")
```

No confundas `=` (asignación) con `==` (comparación). Los valores vacíos, cero y `None` se consideran falsos en un contexto booleano.

## Estructuras simples

Una tupla agrupa valores en un orden fijo; un conjunto conserva elementos únicos; un diccionario relaciona claves con valores.

```python
coordenada = (-34.60, -58.38)
etiquetas = {"python", "inicio", "python"}
tarea = {
    "titulo": "Leer el módulo 1",
    "completada": False,
    "prioridad": 2,
}

print(coordenada[0])
print(etiquetas)
print(tarea["titulo"])
```

Acceder a una clave inexistente con corchetes produce `KeyError`; `tarea.get("fecha")` devuelve `None` de manera segura. `None` representa ausencia de valor y se compara con `is None`.

## Ejemplo guiado: resumen de una compra

```python
producto = input("Producto: ").strip()
precio = float(input("Precio unitario: "))
cantidad = int(input("Cantidad: "))

if precio < 0 or cantidad < 1:
    print("Los datos no son válidos")
else:
    total = precio * cantidad
    compra = (producto, cantidad, total)
    print(f"{compra[1]} × {compra[0]} = ${compra[2]:.2f}")
```

`input()` siempre devuelve texto; por eso convertimos con `float()` e `int()`. Si la entrada no es numérica ocurrirá `ValueError`. Más adelante aprenderás a manejarlo.

## Práctica

1. Convertí una temperatura de Celsius a Fahrenheit con `F = C × 9 / 5 + 32`.
2. Pedí tres notas, calculá el promedio e indicá si es mayor o igual a 6.
3. Creá un diccionario para una película y mostrá una frase con un f-string.
4. Dada una oración, mostrá su longitud y una versión en minúsculas.

## Bitácora 1

Representá una tarea con un diccionario que tenga `id`, `titulo`, `completada` y `etiquetas` (un conjunto). Imprimí un símbolo distinto según su estado. Agregá una segunda etiqueta evitando duplicados.

## Comprobación

¿Podés explicar la diferencia entre valor, variable y tipo? ¿Cuándo elegirías una tupla frente a un diccionario? Si una respuesta no sale sin mirar, escribí un ejemplo mínimo.

# Módulo 02 · Listas y funciones

## Objetivos

- Crear, consultar y modificar listas.
- Recorrer colecciones y construir nuevas.
- Diseñar funciones pequeñas con parámetros y retorno.
- Reconocer mutabilidad, alcance y valores por defecto.

## Listas

Una lista es una secuencia mutable y ordenada. Sus índices comienzan en cero; los negativos cuentan desde el final.

```python
tareas = ["estudiar", "practicar", "descansar"]
tareas.append("repasar")
tareas[0] = "leer"

for indice, tarea in enumerate(tareas, start=1):
    print(indice, tarea)
```

Métodos frecuentes: `append`, `extend`, `insert`, `remove`, `pop`, `sort` y `reverse`. `sorted(lista)` crea otra lista; `lista.sort()` modifica la existente y devuelve `None`.

Los cortes usan `[inicio:fin:paso]`, sin incluir el límite final. Una comprensión expresa transformaciones sencillas:

```python
numeros = [2, 5, 8, 11]
cuadrados_pares = [n ** 2 for n in numeros if n % 2 == 0]
print(cuadrados_pares)
```

Asignar `copia = original` no copia: ambos nombres apuntan a la misma lista. Para una lista plana usá `original.copy()` o `original[:]`. Para estructuras anidadas, investigá `copy.deepcopy`.

## Funciones

Una función encapsula una responsabilidad. Sus parámetros son entradas y `return` produce una salida:

```python
def calcular_total(precios: list[float], descuento: float = 0) -> float:
    """Devuelve el total después de aplicar un descuento entre 0 y 1."""
    if not 0 <= descuento <= 1:
        raise ValueError("El descuento debe estar entre 0 y 1")
    return sum(precios) * (1 - descuento)


total = calcular_total([100, 250, 50], descuento=0.10)
```

Las anotaciones de tipo documentan intención, pero Python no las valida por sí solo. Una variable creada dentro de una función tiene alcance local. Evitá depender de variables globales.

Nunca uses una lista mutable como valor por defecto:

```python
def agregar_etiqueta(etiqueta: str, etiquetas: list[str] | None = None) -> list[str]:
    if etiquetas is None:
        etiquetas = []
    etiquetas.append(etiqueta)
    return etiquetas
```

## Ejemplo guiado: estadísticas

```python
def resumir(datos: list[float]) -> dict[str, float]:
    if not datos:
        raise ValueError("Se necesita al menos un dato")
    return {
        "mínimo": min(datos),
        "máximo": max(datos),
        "promedio": sum(datos) / len(datos),
    }


temperaturas = [18.5, 21.0, 19.8, 23.2]
for clave, valor in resumir(temperaturas).items():
    print(f"{clave}: {valor:.1f}")
```

## Práctica

1. Escribí `es_palindromo(texto)` ignorando espacios y mayúsculas.
2. Escribí `solo_unicos(elementos)` conservando el orden original.
3. Creá `buscar_mayores(personas, edad_minima)` para una lista de diccionarios.
4. Separá una solución larga en funciones de entrada, procesamiento y salida.

## Bitácora 2

Creá funciones `crear_tarea`, `listar_tareas`, `completar_tarea` y `filtrar_pendientes`. Hacé que las funciones devuelvan valores en lugar de imprimir, salvo la función dedicada a presentar resultados. Probá casos con lista vacía e identificador inexistente.

## Idea clave

Una buena función cabe en la cabeza: tiene un nombre que expresa intención, pocas entradas, una salida predecible y una única razón para cambiar.

# Módulo 03 · Módulos, bibliotecas y entornos virtuales

## Objetivos

- Dividir código entre archivos importables.
- Usar la biblioteca estándar y paquetes externos.
- Crear y activar un entorno virtual.
- Diseñar una biblioteca propia sin efectos inesperados.

## Importar y organizar

Cada archivo `.py` es un módulo. Una carpeta con módulos puede formar un paquete; un archivo `__init__.py` explícito sigue siendo conveniente.

```text
bitacora/
├── app.py
└── bitacora/
    ├── __init__.py
    ├── modelos.py
    └── servicios.py
```

En `servicios.py`:

```python
def pendientes(tareas):
    return [tarea for tarea in tareas if not tarea["completada"]]
```

En `app.py`:

```python
from bitacora.servicios import pendientes

print(pendientes([]))
```

Preferí `import modulo` o imports explícitos. `from modulo import *` oculta de dónde vienen los nombres. Python busca módulos en rutas incluidas en `sys.path`; ejecutar desde una carpeta incorrecta suele explicar un `ModuleNotFoundError`.

El bloque principal evita que una demostración se ejecute al importar:

```python
def main() -> None:
    print("Ejecutando la aplicación")


if __name__ == "__main__":
    main()
```

## Biblioteca estándar y paquetes externos

Python incluye módulos como `math`, `statistics`, `datetime`, `json`, `pathlib` y `random`. Consultá primero la biblioteca estándar antes de instalar algo.

Un entorno virtual aísla dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install requests
python -m pip list
deactivate
```

En Windows PowerShell, la activación suele ser `.venv\Scripts\Activate.ps1`. No subas `.venv` a Git. Registrá las dependencias del proyecto y no confundas el intérprete global con el del entorno: `python -c "import sys; print(sys.executable)"` muestra cuál usás.

## Ejemplo guiado: biblioteca de fechas

```python
# bitacora/fechas.py
from datetime import date


def dias_hasta(fecha: date) -> int:
    return (fecha - date.today()).days
```

```python
# app.py
from datetime import date
from bitacora.fechas import dias_hasta

entrega = date.fromisoformat("2027-01-15")
print(dias_hasta(entrega))
```

## Práctica

1. Explorá `statistics.mean` y reemplazá tu promedio manual.
2. Mové las funciones del módulo anterior a un paquete.
3. Creá un entorno, instalá un paquete, verificá su versión y eliminá el entorno.
4. Agregá docstrings a los módulos y funciones públicas.

## Bitácora 3

Separá modelos, lógica de negocio y presentación. `app.py` solo debe coordinar. Asegurate de que `import bitacora.servicios` no imprima ni solicite datos.

# Módulo 04 · Archivos, OS, glob y ZIP

## Objetivos

- Leer y escribir archivos de forma segura.
- Recorrer rutas y patrones.
- Manipular ZIP sin vulnerabilidades comunes.
- Procesar datos sin cargar archivos enormes completos.

## Rutas y contextos

Aunque este módulo incluye `os`, para rutas nuevas suele ser más legible `pathlib`:

```python
from pathlib import Path

ruta = Path("datos") / "tareas.txt"
ruta.parent.mkdir(parents=True, exist_ok=True)

with ruta.open("w", encoding="utf-8") as archivo:
    archivo.write("Aprender context managers\n")

with ruta.open(encoding="utf-8") as archivo:
    for linea in archivo:
        print(linea.rstrip())
```

`with` cierra el recurso incluso si ocurre una excepción. Indicá siempre la codificación. Para datos estructurados, JSON es más robusto que inventar separadores:

```python
import json

datos = [{"id": 1, "titulo": "Practicar", "completada": False}]
Path("tareas.json").write_text(
    json.dumps(datos, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
recuperados = json.loads(Path("tareas.json").read_text(encoding="utf-8"))
```

`os.environ` accede a variables de entorno; `os.replace` permite reemplazos atómicos; `os.walk` recorre árboles. `glob` encuentra patrones:

```python
from glob import glob

for nombre in glob("datos/**/*.json", recursive=True):
    print(nombre)
```

Con `Path`, el equivalente es `Path("datos").rglob("*.json")`.

## Archivos ZIP

```python
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

with ZipFile("respaldo.zip", "w", ZIP_DEFLATED) as zipf:
    for ruta in Path("datos").glob("*.json"):
        zipf.write(ruta, arcname=ruta.name)

with ZipFile("respaldo.zip") as zipf:
    print(zipf.namelist())
```

No extraigas un ZIP no confiable con `extractall()` sin validar nombres: entradas como `../../archivo` podrían escapar del destino. También limitá cantidad y tamaño descomprimido para evitar bombas ZIP.

## Manejo de errores

Capturá excepciones específicas:

```python
from pathlib import Path

try:
    contenido = Path("config.json").read_text(encoding="utf-8")
except FileNotFoundError:
    contenido = "{}"
except PermissionError as error:
    print(f"Sin permiso: {error}")
```

No uses `except Exception: pass`: borra evidencia y complica la depuración.

## Práctica

1. Contá líneas, palabras y caracteres de todos los `.txt` de una carpeta.
2. Renombrá archivos agregando una fecha, primero mostrando una vista previa.
3. Guardá un diccionario en JSON y recuperalo verificando igualdad.
4. Creá un ZIP de respaldo que conserve rutas relativas.

## Bitácora 4

Implementá `guardar_tareas(ruta, tareas)` y `cargar_tareas(ruta)`. Escribí primero a un temporal y reemplazá el original al final para reducir el riesgo de corrupción.

# Módulo 05 · Scripts, terminal y Visual Studio Code

## Objetivos

- Ejecutar módulos y scripts correctamente.
- Recibir argumentos por línea de comandos.
- Configurar el intérprete y depurar en VS Code.
- Crear interfaces de terminal que informen errores útiles.

## De archivo a programa

Ejecutá un archivo con `python app.py` o un módulo dentro de un paquete con `python -m bitacora.cli`. La segunda forma respeta mejor la estructura de imports.

`argparse` crea una interfaz documentada:

```python
import argparse


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gestiona tareas")
    parser.add_argument("titulo", help="Título de la tarea")
    parser.add_argument("-p", "--prioridad", type=int, default=2, choices=[1, 2, 3])
    return parser


def main() -> None:
    argumentos = crear_parser().parse_args()
    print(f"[P{argumentos.prioridad}] {argumentos.titulo}")


if __name__ == "__main__":
    main()
```

Probalo con:

```bash
python app.py --help
python app.py "Preparar entrega" --prioridad 1
```

Los programas comunican resultado mediante códigos de salida: cero significa éxito. `raise SystemExit(2)` finaliza con error. Nunca incluyas contraseñas en argumentos si pueden quedar en el historial; preferí variables de entorno o gestores de secretos.

## VS Code

Instalá la extensión oficial de Python, abrí la carpeta raíz y seleccioná el intérprete de `.venv` desde **Python: Select Interpreter**. Colocá un breakpoint, iniciá **Run and Debug** e inspeccioná variables paso a paso. Configurá argumentos en `.vscode/launch.json` solo si el proyecto lo necesita; evitá compartir rutas personales.

## Práctica

1. Agregá subcomandos `crear`, `listar` y `completar`.
2. Validá que un identificador sea positivo.
3. Ejecutá el CLI desde otra carpeta usando `python -m`.
4. Depurá una excepción deliberada y anotá la cadena de llamadas.

## Bitácora 5

Construí una CLI que persista en JSON. La capa CLI traduce argumentos; la capa de servicios decide reglas; la capa de almacenamiento lee y escribe. Ejecutá cinco operaciones seguidas para comprobar que el estado persiste.

# Módulo 06 · Fundamentos de orientación a objetos

## Objetivos

- Modelar entidades con clases e instancias.
- Definir atributos, métodos e invariantes.
- Usar dataclasses para objetos de datos.
- Elegir composición antes que jerarquías innecesarias.

## Clases y objetos

Una clase define comportamiento compartido; una instancia representa un objeto concreto.

```python
from dataclasses import dataclass


@dataclass
class Tarea:
    id: int
    titulo: str
    completada: bool = False

    def completar(self) -> None:
        self.completada = True

    def renombrar(self, nuevo_titulo: str) -> None:
        limpio = nuevo_titulo.strip()
        if not limpio:
            raise ValueError("El título no puede estar vacío")
        self.titulo = limpio
```

`self` referencia la instancia. `@dataclass` genera inicialización, representación y comparación útiles. La regla del título pertenece al objeto porque protege su estado válido.

Sin `dataclass`, se define `__init__` explícitamente:

```python
class Contador:
    def __init__(self, valor_inicial: int = 0) -> None:
        self._valor = valor_inicial

    @property
    def valor(self) -> int:
        return self._valor

    def incrementar(self) -> None:
        self._valor += 1
```

El guion bajo expresa “uso interno”, no privacidad absoluta. Una propiedad permite exponer lectura sin habilitar modificación directa.

## Composición

```python
class ListaDeTareas:
    def __init__(self) -> None:
        self._tareas: list[Tarea] = []

    def agregar(self, tarea: Tarea) -> None:
        if any(actual.id == tarea.id for actual in self._tareas):
            raise ValueError("El id ya existe")
        self._tareas.append(tarea)

    def pendientes(self) -> list[Tarea]:
        return [tarea for tarea in self._tareas if not tarea.completada]
```

`ListaDeTareas` contiene tareas: esa relación “tiene un” es composición. No todo sustantivo exige una clase; una función y un diccionario siguen siendo opciones válidas.

## Práctica

1. Modelá una cuenta bancaria que no permita saldo negativo.
2. Agregá fecha límite y prioridad a `Tarea`.
3. Compará una solución con dataclass y otra con diccionario.
4. Escribí casos que intenten romper las invariantes.

## Bitácora 6

Reemplazá los diccionarios por `Tarea`. Agregá conversión `a_diccionario` y `desde_diccionario` en el borde de persistencia. Evitá que detalles de JSON invadan el modelo.

# Módulo 07 · Diseño orientado a objetos

## Objetivos

- Asignar responsabilidades y reducir acoplamiento.
- Aplicar abstracción, polimorfismo y composición.
- Usar protocolos para dependencias intercambiables.
- Reconocer señales de un diseño difícil de mantener.

## Responsabilidades y dependencias

Una clase enorme que valida, guarda, imprime y envía correos tiene demasiadas razones para cambiar. Separá reglas del dominio, persistencia e interfaces.

```python
from typing import Protocol


class RepositorioTareas(Protocol):
    def guardar(self, tarea: Tarea) -> None: ...
    def obtener(self, tarea_id: int) -> Tarea | None: ...


class ServicioTareas:
    def __init__(self, repositorio: RepositorioTareas) -> None:
        self.repositorio = repositorio

    def completar(self, tarea_id: int) -> Tarea:
        tarea = self.repositorio.obtener(tarea_id)
        if tarea is None:
            raise LookupError("Tarea inexistente")
        tarea.completar()
        self.repositorio.guardar(tarea)
        return tarea
```

El servicio depende de un comportamiento, no de JSON o una base concreta. Un repositorio en memoria sirve para pruebas y otro en archivos para producción. Esto es inversión de dependencias en una escala práctica.

La herencia expresa “es un” y debe preservar expectativas de la clase base. Preferí composición cuando solo querés reutilizar comportamiento. El polimorfismo permite tratar implementaciones diferentes mediante la misma interfaz.

## Excepciones del dominio

```python
class ErrorDeTarea(Exception):
    """Error base del dominio."""


class TareaNoEncontrada(ErrorDeTarea):
    pass
```

Definir errores específicos evita que la interfaz tenga que interpretar textos. Capturalos en el borde adecuado y traducilos a un mensaje o respuesta HTTP.

## Principios como preguntas

- Responsabilidad única: ¿cuántos motivos distintos hacen cambiar esta unidad?
- Abierto/cerrado: ¿puedo agregar una implementación sin modificar toda la lógica?
- Sustitución: ¿una implementación respeta el contrato esperado?
- Segregación: ¿la interfaz obliga a implementar métodos innecesarios?
- Inversión: ¿la política central depende de detalles externos?

No son mandamientos. Un diseño más abstracto también cuesta; extraé una abstracción cuando exista una variación real o cuando simplifique pruebas.

## Práctica

1. Implementá repositorios en memoria y JSON con el mismo protocolo.
2. Dibujá dependencias entre CLI, servicio, dominio y almacenamiento.
3. Refactorizá una clase con más de una responsabilidad.
4. Escribí el contrato de cada método: entradas, salida, errores y efectos.

## Bitácora 7

Organizá paquetes `dominio`, `aplicacion`, `infraestructura` e `interfaces`. Verificá que el dominio no importe FastAPI, JSON ni detalles de terminal.

# Módulo 08 · pytest y desarrollo guiado por pruebas

## Objetivos

- Escribir pruebas legibles y aisladas con pytest.
- Usar fixtures, parametrización y temporales.
- Aplicar el ciclo rojo, verde, refactor.
- Distinguir pruebas unitarias de integración.

## Primera prueba

Instalá pytest en el entorno del proyecto:

```bash
python -m pip install pytest
python -m pytest
```

Una prueba sigue Preparar, Actuar, Verificar:

```python
import pytest


def test_renombrar_rechaza_titulo_vacio() -> None:
    tarea = Tarea(id=1, titulo="Original")

    with pytest.raises(ValueError, match="vacío"):
        tarea.renombrar("   ")


@pytest.mark.parametrize(
    ("titulo", "esperado"),
    [(" Comprar ", "Comprar"), ("\nLeer\t", "Leer")],
)
def test_renombrar_limpia_extremos(titulo: str, esperado: str) -> None:
    tarea = Tarea(id=1, titulo="Original")
    tarea.renombrar(titulo)
    assert tarea.titulo == esperado
```

Probá comportamiento observable, no detalles internos. Una prueba que falla por cualquier refactor inocuo genera fricción.

## Fixtures y archivos temporales

```python
def test_repositorio_json_persiste(tmp_path) -> None:
    ruta = tmp_path / "tareas.json"
    repositorio = RepositorioJson(ruta)
    repositorio.guardar(Tarea(1, "Probar"))

    recuperada = RepositorioJson(ruta).obtener(1)

    assert recuperada == Tarea(1, "Probar")
```

`tmp_path` aísla archivos. Otras fixtures pueden preparar objetos reutilizables, pero no ocultes tanto que la prueba deje de contar una historia.

## TDD

1. **Rojo:** escribí la prueba más pequeña que exprese el próximo comportamiento y mirala fallar por la razón correcta.
2. **Verde:** implementá lo mínimo para que pase.
3. **Refactor:** mejorá diseño manteniendo todas las pruebas verdes.

TDD no reemplaza diseño, revisión ni pruebas exploratorias. Es una técnica de retroalimentación.

## VS Code

Seleccioná **Python: Configure Tests**, elegí pytest y la carpeta de pruebas. Podrás ejecutar o depurar desde el panel Testing. Confirmá también en terminal: evita depender de una configuración local invisible.

## Práctica

1. Probá alta, búsqueda y finalización de tareas.
2. Parametrizá títulos inválidos.
3. Escribí una prueba de integración de persistencia.
4. Introducí un defecto y comprobá que una prueba relevante falle.

## Bitácora 8

Aplicá TDD para agregar fechas límite. Definí primero qué ocurre con una fecha pasada. Buscá una mayoría de pruebas unitarias rápidas y pocas integraciones significativas; no persigas cobertura numérica sin analizar qué riesgos cubrís.

# Módulo 09 · Concurrencia: hilos y procesos

## Objetivos

- Diferenciar concurrencia, paralelismo y asincronía.
- Elegir hilos para espera de E/S y procesos para CPU.
- Evitar condiciones de carrera y bloqueos.
- Medir antes de agregar complejidad.

## Elegir la herramienta

Una tarea limitada por E/S pasa tiempo esperando red o disco: los hilos pueden solapar esas esperas. Una tarea limitada por CPU realiza cálculo intensivo: procesos separados pueden aprovechar varios núcleos y evitan las limitaciones del GIL de CPython para bytecode. Crear trabajadores tiene costo; para tareas pequeñas, lo secuencial gana.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen


def obtener_tamano(url: str) -> tuple[str, int]:
    with urlopen(url, timeout=10) as respuesta:
        return url, len(respuesta.read())


urls = ["https://www.python.org", "https://docs.python.org/3/"]
with ThreadPoolExecutor(max_workers=4) as ejecutor:
    futuros = [ejecutor.submit(obtener_tamano, url) for url in urls]
    for futuro in as_completed(futuros):
        try:
            print(futuro.result())
        except Exception as error:
            print(f"Falló una descarga: {error}")
```

Para CPU:

```python
from concurrent.futures import ProcessPoolExecutor


def suma_cuadrados(limite: int) -> int:
    return sum(n * n for n in range(limite))


if __name__ == "__main__":
    with ProcessPoolExecutor() as ejecutor:
        print(list(ejecutor.map(suma_cuadrados, [500_000] * 4)))
```

El guard de `__main__` es esencial con multiprocessing, especialmente en Windows y macOS. Los argumentos deben poder serializarse. Las excepciones aparecen al obtener el resultado del futuro.

## Estado compartido

Dos hilos que modifican un valor pueden intercalarse. Minimizá estado mutable compartido; preferí pasar mensajes y devolver resultados. Cuando sea inevitable, usá primitivas como `Lock` y mantené la sección crítica pequeña. Adquirir locks en orden inconsistente puede producir deadlock.

## Medición y límites

Definí timeout, tratá fallos parciales y limitá trabajadores. “Más” no siempre acelera: puede saturar red, memoria, API o disco. Medí con `time.perf_counter()` varias veces y compará resultados correctos, no solo duración.

## Práctica

1. Descargá varias páginas de prueba secuencialmente y con hilos.
2. Calculá números primos secuencialmente y con procesos.
3. Provocá una carrera en un contador y corregila.
4. Diseñá qué hacer si 2 de 20 tareas fallan.

## Bitácora 9

Generá reportes de varios archivos en paralelo. Cada trabajador lee y devuelve estadísticas; un coordinador único combina y escribe. No permitas que múltiples trabajadores reescriban el mismo JSON.

# Módulo 10 · Integración continua y calidad automatizada

## Objetivos

- Integrar cambios pequeños en un repositorio compartido.
- Automatizar formato, análisis y pruebas.
- Leer fallos de CI y reproducirlos localmente.
- Diseñar una canalización rápida y determinista.

## Qué es integración continua

CI ejecuta verificaciones ante cada cambio para detectar errores temprano. No es “compilar Python” en el sentido tradicional: suele incluir instalación reproducible, chequeo de sintaxis, estilo, tipos, pruebas y construcción de paquetes.

Una estrategia básica:

```text
cambio pequeño → commit → push → checks automáticos → revisión → integración
```

Ejemplo de GitHub Actions:

```yaml
name: calidad
on:
  push:
  pull_request:

jobs:
  pruebas:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: python -m pip install -r requirements-dev.txt
      - run: python -m compileall -q src
      - run: python -m pytest
```

Fijá versiones de acciones a una versión confiable o SHA según la política del equipo. Nunca imprimas secretos. Un workflow debe partir de un checkout limpio y no depender de archivos ignorados.

## Fallos útiles

Si CI falla:

1. Identificá el primer error relevante, no el último efecto en cadena.
2. Compará versión de Python, sistema y dependencias.
3. Reproducí el comando exacto localmente.
4. Corregí la causa, agregá una prueba si faltaba y volvé a ejecutar todo.

Evitá pruebas que dependan de hora real, orden no garantizado o red externa. Inyectá reloj y simulá fronteras cuando corresponda.

## Práctica

1. Creá un workflow que ejecute pytest.
2. Agregá chequeos para dos versiones de Python con una matriz.
3. Rompé una prueba, interpretá el log y corregila.
4. Añadí una insignia solo después de que el workflow sea estable.

## Bitácora 10

Definí una única orden local —por ejemplo `python -m pytest`— equivalente al núcleo de CI. Documentá requisitos y hacé que una instalación limpia pueda ejecutar los checks.

# Módulo 11 · APIs REST con FastAPI

## Objetivos

- Comprender recursos, métodos HTTP y códigos de estado.
- Crear endpoints tipados con FastAPI.
- Validar datos y separar API de lógica.
- Probar la API sin depender de un servidor externo.

## Primera API

Instalá las herramientas en un entorno:

```bash
python -m pip install fastapi "uvicorn[standard]"
```

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Bitácora API")


class TareaEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=120)


class TareaSalida(TareaEntrada):
    id: int
    completada: bool


tareas: dict[int, TareaSalida] = {}


@app.post("/tareas", response_model=TareaSalida, status_code=status.HTTP_201_CREATED)
def crear_tarea(entrada: TareaEntrada) -> TareaSalida:
    tarea_id = max(tareas, default=0) + 1
    tarea = TareaSalida(id=tarea_id, titulo=entrada.titulo, completada=False)
    tareas[tarea_id] = tarea
    return tarea


@app.get("/tareas/{tarea_id}", response_model=TareaSalida)
def obtener_tarea(tarea_id: int) -> TareaSalida:
    if tarea_id not in tareas:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tareas[tarea_id]
```

Ejecutá:

```bash
uvicorn bitacora.api:app --reload
```

Visitá `/docs` para OpenAPI interactivo. `--reload` es solo desarrollo.

## Diseño HTTP

- `GET` consulta y no debe alterar estado.
- `POST` crea o dispara una operación no idempotente.
- `PUT` reemplaza; `PATCH` modifica parcialmente.
- `DELETE` elimina.
- `200` éxito, `201` creación, `204` éxito sin cuerpo, `400` solicitud inválida, `404` ausencia y `409` conflicto.

Los modelos de transporte no tienen por qué ser las clases del dominio. Traducí errores del servicio en respuestas HTTP. Inyectá dependencias para repositorios, autenticación y configuración.

## Producción responsable

Definí timeouts, límites, autenticación y CORS según consumidores reales. No devuelvas trazas ni secretos. Una API pública necesita versionado, observabilidad y política de cambios. FastAPI valida forma y tipos, no todas las reglas de negocio.

## Pruebas

```python
from fastapi.testclient import TestClient
from bitacora.api import app

cliente = TestClient(app)


def test_crear_tarea() -> None:
    respuesta = cliente.post("/tareas", json={"titulo": "Probar API"})
    assert respuesta.status_code == 201
    assert respuesta.json()["titulo"] == "Probar API"
```

## Práctica

1. Implementá listar, completar y eliminar.
2. Agregá filtros de estado y paginación.
3. Probá entradas vacías e identificadores inexistentes.
4. Reemplazá el diccionario global por tu servicio.

## Bitácora 11

Exponé el servicio existente sin duplicar reglas. Revisá `/openapi.json`, escribí pruebas de contrato y comprobá que el estado global no contamine pruebas.

# Módulo 12 · Git para trabajar con confianza

## Objetivos

- Comprender repositorio, commit, rama y remoto.
- Crear commits enfocados y resolver conflictos.
- Colaborar mediante ramas y pull requests.
- Evitar publicar secretos o artefactos.

## Modelo mental

Git registra instantáneas. Tu directorio de trabajo contiene cambios; el área de preparación selecciona qué entrará al próximo commit; el repositorio guarda el historial.

```bash
git init
git status
git add src/bitacora/modelos.py tests/test_modelos.py
git diff --staged
git commit -m "Agrega validación de títulos"
git log --oneline
```

Revisá el diff antes de preparar y antes de confirmar. Un commit debe expresar una idea completa y dejar el proyecto coherente.

## Ramas y colaboración

```bash
git switch -c feature/fechas-limite
git push -u origin feature/fechas-limite
```

Actualizá referencias con `git fetch`. Integrar cambios puede producir conflictos: abrí cada archivo, entendé ambas intenciones, resolvé marcadores, ejecutá pruebas y recién entonces confirmá. No elijas “el nuestro” o “el de ellos” sin leer.

Un pull request facilita conversación y checks. Describí problema, solución, forma de probar y decisiones. Mantenelo pequeño.

## Seguridad e higiene

`.gitignore` evita archivos no rastreados como `.venv/`, `__pycache__/`, `.env` y datos locales. No elimina secretos ya confirmados. Si publicaste uno, revocalo y rotalo primero; luego limpiá historial con ayuda del equipo.

No uses comandos destructivos copiándolos a ciegas. Antes de reescribir historial compartido, entendé el impacto y coordiná.

## Práctica

1. Creá un repositorio y tres commits enfocados.
2. Inspeccioná diferencias de trabajo y staged.
3. Simulá y resolvé un conflicto en dos ramas.
4. Escribí una descripción de PR reproducible.

## Bitácora 12

Versioná el proyecto. Excluí entorno, cachés, configuración local y datos generados. Usá una rama por cambio, commits descriptivos y revisión del diff.

# Módulo 13 · Dependencias, entornos y Poetry

## Objetivos

- Separar dependencias de producción y desarrollo.
- Crear proyectos y lockfiles con Poetry.
- Ejecutar comandos dentro del entorno correcto.
- Comprender rangos, resolución y reproducibilidad.

## Dos niveles de dependencia

Tu proyecto declara restricciones compatibles; el lock registra resoluciones exactas para instalaciones repetibles. Una biblioteca suele permitir rangos razonables; una aplicación despliega versiones verificadas.

Con Poetry instalado según su documentación oficial:

```bash
poetry new bitacora
cd bitacora
poetry add fastapi
poetry add --group dev pytest ruff mypy
poetry run pytest
poetry install
```

`pyproject.toml` centraliza metadatos y herramientas; `poetry.lock` debe versionarse en aplicaciones. `poetry update` busca versiones nuevas dentro de restricciones y cambia el lock; `poetry install` respeta el lock.

No mezcles al azar `pip` y Poetry dentro del mismo entorno. Verificá `poetry env info` y `poetry run python --version`.

Ejemplo conceptual:

```toml
[project]
name = "bitacora"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.100"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

La sintaxis exacta y el flujo de empaquetado evolucionan; consultá la documentación de la versión instalada. Evitá restricciones excesivamente amplias sin CI que pruebe compatibilidad.

## Dependencias confiables

Antes de agregar un paquete, evaluá mantenimiento, licencia, seguridad, tamaño y si la estándar alcanza. Actualizá de manera frecuente y revisable. Un lock no garantiza seguridad: solo repetibilidad.

## Práctica

1. Migrá un proyecto pequeño a `pyproject.toml`.
2. Separá pytest y herramientas de estilo en un grupo dev.
3. Recreá el entorno desde cero usando el lock.
4. Explicá qué archivo cambia con `add`, `install` y `update`.

## Bitácora 13

Administrá API, tests y herramientas con Poetry. Documentá una secuencia desde clon limpio hasta servidor funcionando. Verificá que no dependa de paquetes instalados globalmente.

# Módulo 14 · Plantillas, tipado y distribución

## Objetivos

- Estructurar proyectos reproducibles con Cookiecutter.
- Añadir tipos gradualmente y analizarlos.
- Construir paquetes con estándares modernos.
- Entender el papel actual de setuptools.

## Cookiecutter

Cookiecutter genera una estructura a partir de una plantilla con variables. Es útil cuando un equipo crea muchos proyectos similares, pero una plantilla envejece: mantenela pequeña, probada y documentada.

```bash
cookiecutter ruta-o-url-de-la-plantilla
```

Nunca ejecutes hooks de una plantilla desconocida sin inspeccionarlos: pueden ejecutar código con tus permisos. Una plantilla propia puede incluir `src/`, `tests/`, `pyproject.toml`, CI y README, sin imponer servicios que el proyecto no necesita.

## Tipado gradual

```python
from collections.abc import Iterable


def titulos_pendientes(tareas: Iterable[Tarea]) -> list[str]:
    return [tarea.titulo for tarea in tareas if not tarea.completada]
```

Un analizador como mypy encuentra inconsistencias sin ejecutar:

```bash
mypy src
```

Los tipos mejoran contratos y herramientas, pero no validan datos externos en runtime. Evitá llenar el código de `Any`: desactiva comprobación. Usá `T | None`, genéricos, `Protocol` y alias cuando hagan más clara la intención.

## Empaquetado moderno

Setuptools puede actuar como backend de construcción declarado en `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.build_meta"

[project]
name = "bitacora"
version = "0.1.0"
description = "Gestor de tareas educativo"
requires-python = ">=3.12"

[project.scripts]
bitacora = "bitacora.cli:main"
```

Construí un wheel y un paquete fuente con:

```bash
python -m pip install build
python -m build
python -m pip install dist/bitacora-0.1.0-py3-none-any.whl
```

No subas a un índice real durante la práctica. Probá el artefacto en un entorno limpio. No agregues `setup.py` salvo que necesites compatibilidad específica; el estándar moderno concentra metadatos en `pyproject.toml`.

## Práctica

1. Tipá una función sin usar `Any`.
2. Ejecutá un analizador y corregí errores reales.
3. Definí un comando de consola.
4. Construí e instalá el wheel en otro entorno.

## Bitácora 14

Creá una plantilla mínima basada en la estructura que ya demostró servir. Tipá las fronteras públicas y construí un wheel. Comprobá que `bitacora --help` funcione después de instalarlo.

# Módulo 15 · Estilo, estándares y logging

## Objetivos

- Automatizar formato y lint.
- Escribir código legible según convenciones.
- Registrar eventos con niveles y contexto.
- Evitar filtrar información sensible en logs.

## Calidad automatizada

PEP 8 orienta estilo; un formateador elimina discusiones mecánicas y un linter encuentra errores y patrones riesgosos. Ruff puede cubrir gran parte del flujo:

```bash
ruff format .
ruff check .
ruff check . --fix
```

Revisá los cambios automáticos. Configurá herramientas en `pyproject.toml` y ejecutalas en CI. Nombres claros, funciones pequeñas y comentarios sobre el “por qué” importan más que trucos compactos.

## Logging

`print` es salida para el usuario; logging es telemetría para operar y depurar:

```python
import logging

logger = logging.getLogger(__name__)


def completar_tarea(tarea_id: int, servicio: ServicioTareas) -> None:
    logger.info("Completando tarea", extra={"tarea_id": tarea_id})
    try:
        servicio.completar(tarea_id)
    except TareaNoEncontrada:
        logger.warning("Tarea no encontrada", extra={"tarea_id": tarea_id})
        raise
```

La aplicación, no cada biblioteca, configura handlers y formato:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
```

Niveles: `DEBUG` para diagnóstico detallado, `INFO` para hitos normales, `WARNING` para una situación inesperada recuperable, `ERROR` para una operación fallida y `CRITICAL` para fallos graves. `logger.exception()` dentro de un `except` agrega la traza.

No registres contraseñas, tokens, documentos completos ni datos personales innecesarios. En servicios, preferí logs estructurados y un identificador de correlación. Evitá duplicar el mismo error en todas las capas.

## Práctica

1. Configurá formato y lint en `pyproject.toml`.
2. Corregí una función compleja guiándote por legibilidad.
3. Agregá logs a una operación exitosa y una fallida.
4. Revisá qué campos serían sensibles.

## Bitácora 15

Aplicá formato, lint, tipos y tests con órdenes documentadas. Agregá logs en CLI y API sin cambiar reglas del dominio. Simulá un error y verificá que el log permita seguirlo sin exponer el contenido de las tareas.

# Módulo 16 · Docker y entrega consistente

## Objetivos

- Comprender imágenes, contenedores y registros.
- Crear una imagen pequeña y reproducible.
- Configurar la aplicación mediante el entorno.
- Ejecutar como usuario sin privilegios y probar el artefacto.

## Imagen y contenedor

Una imagen es una plantilla inmutable por capas; un contenedor es un proceso aislado creado desde ella. Docker mejora consistencia, pero no es una máquina virtual completa ni elimina la necesidad de seguridad y observabilidad.

Ejemplo de `Dockerfile`:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-root

COPY src ./src
RUN poetry install --only main --no-interaction

USER app
EXPOSE 8000
CMD ["uvicorn", "bitacora.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Ajustá el flujo a la versión de Poetry y probalo: algunos proyectos exportan requirements o usan construcción multietapa para evitar herramientas de build en la imagen final.

`.dockerignore`:

```text
.git
.venv
__pycache__
.pytest_cache
.mypy_cache
.ruff_cache
tests
dist
.env
```

Construcción y ejecución:

```bash
docker build -t bitacora:0.1.0 .
docker run --rm -p 8000:8000 --env-file .env bitacora:0.1.0
```

No copies secretos dentro de la imagen ni los escribas en el Dockerfile. Inyectalos al ejecutar mediante una solución apropiada. Fijá imágenes base con una estrategia de actualización y analizá vulnerabilidades.

## Datos y operación

El sistema de archivos del contenedor es descartable. Usá volúmenes o servicios externos para datos persistentes. Mantené un proceso principal por contenedor, capturá señales para cierre limpio y escribí logs a stdout/stderr.

Un healthcheck debe comprobar capacidad real sin causar carga. En producción, limitá recursos, usá HTTPS en el borde y ejecutá migraciones de manera explícita.

## Práctica

1. Construí la imagen y consultá `/docs`.
2. Inspeccioná capas y tamaño.
3. Ejecutá como usuario no root y verificá permisos.
4. Cambiá configuración sin reconstruir.
5. Detené el contenedor y verificá qué datos persisten.

## Bitácora 16

Empaquetá la API, probá la imagen desde cero y documentá comandos de build, ejecución y verificación. El entregable final debe pasar tests antes de construir y responder una solicitud de salud después de arrancar.

# Proyecto final · Bitácora lista para compartir

Construí una versión integrada que demuestre el recorrido. Evitá agregar características hasta consolidar las esenciales.

## Requisitos funcionales

- Crear, listar, consultar, completar y eliminar tareas.
- Validar título, prioridad y fecha límite.
- Persistir mediante una implementación desacoplada.
- Exponer CLI y API sin duplicar reglas.
- Generar un reporte concurrente de tareas.

## Requisitos técnicos

- Paquete con estructura `src` y configuración en `pyproject.toml`.
- Tipos en la API pública y excepciones de dominio.
- Pruebas unitarias y de integración deterministas.
- Formato, lint, tipos y tests en integración continua.
- Logs útiles sin datos sensibles.
- Imagen Docker ejecutada sin privilegios.
- README con instalación, arquitectura, decisiones y comandos.

## Criterios de terminado

1. Un clon limpio puede instalar y ejecutar los checks siguiendo el README.
2. La API documenta su contrato y devuelve códigos coherentes.
3. Los errores de entrada no producen trazas para consumidores.
4. La lógica del dominio funciona sin FastAPI ni archivos reales.
5. El wheel se instala y el contenedor inicia.
6. Cada cambio importante está representado por commits enfocados.

## Secuencia sugerida

Primero escribí historias pequeñas y criterios de aceptación. Modelá el dominio con pruebas; agregá repositorios; conectá CLI y API; automatizá calidad; construí el paquete; finalmente creá y verificá el contenedor. Ante cada falla, reducila a un ejemplo reproducible.

# Apéndice A · Guía para resolver problemas

Cuando algo falla:

1. Leé el error completo desde la primera línea relevante hasta el final.
2. Identificá archivo, línea, tipo de excepción y mensaje.
3. Formulá qué esperabas y qué ocurrió.
4. Reducí el problema a la entrada más pequeña.
5. Comprobá versión, intérprete, carpeta actual y entorno.
6. Consultá documentación oficial.
7. Cambiá una causa posible por vez y repetí.
8. Convertí el defecto en una prueba cuando tenga sentido.

Errores frecuentes:

- `SyntaxError`: Python no pudo interpretar la sintaxis indicada.
- `IndentationError`: los bloques no tienen indentación coherente.
- `NameError`: el nombre no existe en ese alcance.
- `TypeError`: la operación recibió un tipo incompatible.
- `ValueError`: el tipo es correcto, el valor no.
- `KeyError` o `IndexError`: la clave o posición no existe.
- `ModuleNotFoundError`: paquete no instalado, import incorrecto o intérprete equivocado.

No pegues datos sensibles al pedir ayuda. Compartí un ejemplo mínimo, versiones, comando exacto y traza en texto.

# Apéndice B · Hoja de referencia

```python
# Colecciones
lista = [1, 2, 3]
tupla = (1, 2)
conjunto = {1, 2}
diccionario = {"clave": "valor"}

# Recorrido
for indice, valor in enumerate(lista):
    print(indice, valor)

# Función
def transformar(valor: int) -> str:
    return str(valor)

# Excepción
try:
    numero = int("42")
except ValueError as error:
    print(error)

# Archivo
from pathlib import Path
texto = Path("archivo.txt").read_text(encoding="utf-8")

# Punto de entrada
def main() -> None:
    ...

if __name__ == "__main__":
    main()
```

Comandos de diagnóstico:

```bash
python --version
python -c "import sys; print(sys.executable)"
python -m pip --version
python -m pytest
git status
docker version
```

# Cierre

Aprender programación es acumular ciclos de hipótesis, código y retroalimentación. Volvé sobre Bitácora después de unas semanas: simplificá un diseño, mejorá una prueba y explicá una decisión. La señal de progreso no es escribir más líneas, sino resolver problemas con menos incertidumbre y verificar que la solución hace lo que promete.
