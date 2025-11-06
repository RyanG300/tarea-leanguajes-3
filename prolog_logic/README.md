# Probar las reglas Prolog desde Python

Este pequeño helper permite ejecutar consultas Prolog desde Python usando SWI‑Prolog (`swipl`).

Requisitos
- macOS (o cualquier OS donde tengas swipl)
- SWI-Prolog (recomendado instalar con Homebrew):

```sh
brew install swi-prolog
```

Archivos creados
- `prolog_client.py`: cliente que invoca `swipl` y devuelve resultados como listas de Python (JSON desde Prolog).
- `test_from_python.py`: script con ejemplos para `menu_por_calorias`, `menu_vegetariano` y `menu_tipo_carne`.

Cómo usar
1. Asegúrate de estar en la carpeta del proyecto (donde están `menu_db.pl`, `menu_generator.pl`, `menu_filters.pl`).
2. Ejecuta el script de prueba:

```sh
python3 test_from_python.py
```

Notas
- El cliente asume que los archivos Prolog tienen estos nombres y están junto al script. Si tus archivos están en otra ubicación, pásalos al constructor `PrologClient(prolog_files=[...])`.
- El script usa la librería `library(http/json)` de SWI-Prolog para emitir resultados en JSON; SWI-Prolog estándar incluye esa librería.

Si quieres que el cliente devuelva soluciones una por una (streaming) o que acepte consultas interactivas, puedo ampliarlo con esas opciones.
