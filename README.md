# Dashboard USD/MXN

Dashboard interactivo que muestra la evolución del tipo de cambio USD → MXN, construido con **FastAPI**, **Chart.js** y datos desde un archivo CSV.

## Requisitos

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) (recomendado) o `pip`

## Instalación y ejecución

### Con `uv` (recomendado)

```bash
uv venv
source .venv/bin/activate        # bash / zsh
# overlay use .venv/bin/activate.nu  # nushell
uv pip install -e .
fastapi dev main.py
```

### Con `pip`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
fastapi dev main.py
```

El dashboard estará disponible en **http://127.0.0.1:8000**.

## Estructura del proyecto

```
├── main.py                  # Backend FastAPI
├── pyproject.toml           # Dependencias del proyecto
├── data/
│   └── usd_mxn.csv          # Datos del tipo de cambio
└── templates/
    └── dashboard.html        # Frontend (HTML + CSS + JS)
```

## API

| Endpoint               | Descripción                                           |
| ---------------------- | ----------------------------------------------------- |
| `GET /`                | Sirve el dashboard HTML                               |
| `GET /api/tipo-cambio` | Datos JSON, acepta `?desde=` y `?hasta=` (YYYY-MM-DD) |
