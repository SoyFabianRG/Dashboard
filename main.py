import csv
from datetime import date
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

app = FastAPI(title="Dashboard USD/MXN")

CSV_PATH = Path(__file__).parent / "data" / "usd_mxn.csv"
TEMPLATE_PATH = Path(__file__).parent / "templates" / "dashboard.html"


def leer_csv() -> list[dict]:
    """Lee el archivo CSV y devuelve una lista de diccionarios."""
    datos: list[dict] = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            datos.append(
                {
                    "fecha": row["fecha"],
                    "tipo_cambio": float(row["tipo_cambio"]),
                }
            )
    return datos


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Sirve el dashboard HTML."""
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.get("/api/tipo-cambio")
async def tipo_cambio(
    desde: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    hasta: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
):
    """Devuelve los datos del tipo de cambio, opcionalmente filtrados por rango de fechas."""
    datos = leer_csv()

    if desde:
        fecha_desde = date.fromisoformat(desde)
        datos = [d for d in datos if date.fromisoformat(d["fecha"]) >= fecha_desde]

    if hasta:
        fecha_hasta = date.fromisoformat(hasta)
        datos = [d for d in datos if date.fromisoformat(d["fecha"]) <= fecha_hasta]

    return datos
