## Instalación y ejecución

### Instalación recomendada (brew + pipx + venv)

Para evitar problemas de `pip` global con Homebrew debido al error `externally-managed-environment`, se recomienda usar `pipx` para instalar herramientas globales y `uv sync` para el entorno virtual del proyecto.

Instalación:

```bash
brew install python pipx ruff
pipx ensurepath
pipx install basedpyright
```

Notas:

- `ruff`: lint y formato.
- `basedpyright`: LSP para autocompletado y diagnosticos.
- `pipx`: instala herramientas globales sin ensuciar el Python global.

### Ejecución con `uv` (recomendado)

Para ejecutar manualmente:

```bash
uv venv
source .venv/bin/activate # bash / zsh
overlay use .venv/bin/activate.nu # nushell
uv pip install -e .
fastapi dev main.py
```

### Ejecución con `pip`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
fastapi dev main.py
```

### Ejecución automática

```bash
uv sync
uv run fastapi dev main.py
```

Nota:

- `uv sync` prepara el entorno virtual y sincroniza dependencias.
- `uv venv` solo crea el entorno virtual sin instalar dependencias.
- `uv run` ejecuta comandos dentro del entorno virtual sin necesidad de activarlo manualmente.
