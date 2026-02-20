# Dashboard Afluencia del Metro

Dashboard interactivo que muestra la evolución del tipo de cambio USD → MXN, construido con **FastAPI**, **Chart.js** y datos desde un archivo CSV.

## Ejecución

Para ejecutar:

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

El dashboard estará disponible en **http://127.0.0.1:8000**.

## Requisitos

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) (recomendado) o `pip`

## Instalación y ejecución

### Instalacion recomendada (brew + pipx + venv)

Para evitar problemas de `pip` global con Homebrew:

```bash
brew install python pipx ruff
pipx ensurepath
pipx install basedpyright
```

Notas:

- `ruff`: lint y formato.
- `basedpyright`: LSP para autocompletado y diagnosticos.
- `pipx`: instala herramientas globales sin ensuciar el Python global.

### Con `uv` (recomendado)

```bash
uv venv
#source .venv/bin/activate        # bash / zsh
overlay use .venv/bin/activate.nu  # nushell
uv pip install -e .
fastapi dev main.py
```

Que instala esto:

- `pytest`: ejecucion de tests.
- `debugpy`: backend de debugging para `nvim-dap-python`.

### Con `pip`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
fastapi dev main.py
```

### Flujo diario (cada vez que trabajes)

```bash
cd tu-proyecto
overlay use .venv/bin/activate.nu
nvim .
```

### NVIM

Dentro de Neovim:

1. `<leader>cv` o `:VenvSelect`para seleccionar `.venv` (primera vez por proyecto).
2. Abre un archivo `.py`.
3. Usa estos atajos:
   - `<leader>pr`: ejecutar archivo actual.
   - `<leader>pt`: correr `pytest` del archivo actual.
   - `<leader>pT`: correr toda la suite de tests.
   - `<leader>dPt`: debug del test actual.
   - `<leader>dPc`: debug de la clase de tests.

Este dashboard usa datos hasta el 31 de enero de 2026
