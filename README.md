# EduLib

EduLib es una biblioteca educativa organizada por materias.

## Estructura

- `mathematics`: herramientas de matemáticas.
- `economics`: herramientas de economía.
- `text`: herramientas para trabajar con texto.
- `physics`: herramientas de física.
- `chemistry`: herramientas de química.

## Desarrollo

Activa el entorno virtual y ejecuta las pruebas con:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest discover -s tests
```
## Importación

```python
import edulib as edl
```