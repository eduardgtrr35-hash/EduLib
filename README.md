# EduLib

EduLib es una biblioteca de Python para proyectos personales y de uso público, organizada por materias.

## Estructura

- `mathematics`: herramientas de matemáticas y álgebra.
- `economics`: herramientas de economía.
- `text`: herramientas para trabajar con texto.
- `physics`: herramientas de física.
- `chemistry`: herramientas de química.

## Instalación

Instala la biblioteca desde el repositorio local:

```powershell
python -m pip install .
```

El módulo de álgebra requiere SymPy. Para instalarlo junto con EduLib, usa el extra `math`:

```powershell
python -m pip install ".[math]"
```

## Uso

Las funciones matemáticas devuelven sus resultados para que puedan guardarse o combinarse con otras operaciones:

```python
import edulib as edl

resultado = edl.sumar(2, 3)
print(resultado)  # 5
```

## Desarrollo

Instala las dependencias de desarrollo y ejecuta las pruebas con:

```powershell
python -m pip install -e ".[math]"
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```
