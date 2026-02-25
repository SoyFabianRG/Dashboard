from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles  # Importación necesaria para servir archivos estáticos
import pandas as pd

# 1. Definir rutas (usando la estructura de carpetas profesional)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = BASE_DIR / "data" / "processed" / "clean_afluencia_metro.csv"
TEMPLATE_PATH = BASE_DIR / "templates" / "dashboard.html"
STATIC_DIR = BASE_DIR / "static"  # Ruta a la carpeta estática en la raíz

# Variable global para mantener el dataset en memoria (RAM)
# Esto hace que las consultas del dashboard sean de milisegundos
df_metro = pd.DataFrame()

# 2. Lifespan de FastAPI (Buena práctica moderna)
# Esto se ejecuta ANTES de que el servidor empiece a recibir usuarios
@asynccontextmanager
async def lifespan(app: FastAPI):
    global df_metro
    print(f"Buscando datos limpios en: {CSV_PATH}")
    if CSV_PATH.exists():
        df_metro = pd.read_csv(CSV_PATH)
        # Asegurarnos de que la columna de fecha funcione como tiempo
        df_metro['fecha'] = pd.to_datetime(df_metro['fecha'])
        print(f"¡Datos cargados en memoria! {len(df_metro)} registros listos.")
    else:
        print("ADVERTENCIA: No se encontró clean_afluencia_metro.csv.")
    yield
    # Aquí iría el código de apagado si fuera necesario
    df_metro = pd.DataFrame()

app = FastAPI(title="Dashboard Afluencia Metro CDMX", lifespan=lifespan)

# <-- Montamos la carpeta para que FastAPI sirva el CSS y JS correctamente -->
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 3. Función auxiliar para evitar repetir código (DRY)
# CORRECCIÓN: Agregamos Optional[str] para que el tipado coincida con los endpoints
def filter_by_date(df: pd.DataFrame, start_date: Optional[str], end_date: Optional[str]) -> pd.DataFrame:
    """Filtra el DataFrame por un rango de fechas si se proporcionan."""
    filtered_df = df.copy()
    if start_date:
        filtered_df = filtered_df[filtered_df['fecha'] >= pd.to_datetime(start_date)]
    if end_date:
        filtered_df = filtered_df[filtered_df['fecha'] <= pd.to_datetime(end_date)]
    return filtered_df

# --- ENDPOINTS (RUTAS) ---

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Sirve la interfaz gráfica (HTML)."""
    # Al leer el HTML aquí, las etiquetas <link> y <script> pedirán los archivos a /static/
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    return HTMLResponse(content=html)

@app.get("/api/kpis")
async def get_kpis(
    start_date: Optional[str] = Query(None, alias="desde"),
    end_date: Optional[str] = Query(None, alias="hasta"),
):
    """Devuelve los indicadores principales (Tarjetas superiores del Dashboard)."""
    if df_metro.empty:
        return {}
    
    df_filtered = filter_by_date(df_metro, start_date, end_date)
    if df_filtered.empty:
        return {}

    # Feature Engineering rápido con Pandas
    total_users = int(df_filtered['afluencia'].sum())
    daily_avg = int(df_filtered.groupby('fecha')['afluencia'].sum().mean())
    
    # Encontrar el valor máximo (idxmax nos da el nombre de la estación/línea)
    top_station = df_filtered.groupby('estacion')['afluencia'].sum().idxmax()
    top_line = df_filtered.groupby('linea')['afluencia'].sum().idxmax()

    return {
        "total_afluencia": total_users,
        "promedio_diario": daily_avg,
        "estacion_top": top_station,
        "linea_top": top_line
    }

@app.get("/api/trend")
async def get_trend(
    start_date: Optional[str] = Query(None, alias="desde"),
    end_date: Optional[str] = Query(None, alias="hasta"),
):
    """Agrupa la afluencia total por día (Para la gráfica de líneas)."""
    if df_metro.empty:
        return []
    
    df_filtered = filter_by_date(df_metro, start_date, end_date)
    
    # Agrupar por fecha y sumar afluencia
    trend = df_filtered.groupby('fecha')['afluencia'].sum().reset_index()
    
    # Convertir la fecha de vuelta a string para que el navegador la entienda (JSON)
    trend['fecha'] = trend['fecha'].dt.strftime('%Y-%m-%d')
    
    # Convertir el DataFrame a una lista de diccionarios
    return trend.to_dict(orient='records')

@app.get("/api/lines")
async def get_lines_distribution(
    start_date: Optional[str] = Query(None, alias="desde"),
    end_date: Optional[str] = Query(None, alias="hasta"),
):
    """Agrupa la afluencia total por línea (Para una nueva gráfica de barras o pastel)."""
    if df_metro.empty:
        return []
    
    df_filtered = filter_by_date(df_metro, start_date, end_date)
    
    # Agrupar por línea
    lines = df_filtered.groupby('linea')['afluencia'].sum().reset_index()
    # Ordenar de mayor a menor afluencia
    lines = lines.sort_values(by='afluencia', ascending=False)
    
    return lines.to_dict(orient='records')