import os
import requests
import pandas as pd
from pathlib import Path

def obtener_datos_cdmx(resource_id: str, limite: int = 1000) -> pd.DataFrame:
    """
    Conecta a la API de Datos Abiertos CDMX (CKAN) y devuelve un DataFrame.
    
    Args:
        resource_id (str): El ID único del recurso (se obtiene de la URL del dataset).
        limite (int): Número máximo de registros a descargar.
    """
    # Endpoint base de la API de CKAN para búsquedas
    url = "https://datos.cdmx.gob.mx/api/3/action/datastore_search"
    
    params = {
        "resource_id": resource_id,
        "limit": limite
    }
    
    try:
        print(f"Conectando a API CDMX (Recurso: {resource_id})...")
        response = requests.get(url, params=params)
        response.raise_for_status() # Lanza error si la conexión falla (ej. 404, 500)
        
        data = response.json()
        
        # La estructura de CKAN devuelve los datos en ['result']['records']
        if "result" in data and "records" in data["result"]:
            records = data["result"]["records"]
            df = pd.DataFrame(records)
            return df
        else:
            print("No se encontraron registros en la respuesta.")
            return pd.DataFrame()
            
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # ID del dataset de Afluencia del Metro CDMX
    ID_EJEMPLO = "cce544e1-dc6b-42b4-bc27-0d8e6eb3ed72"
    
    # En la vida real, el metro tiene millones de registros. 
    # Para tu portafolio, bajemos una muestra representativa (ej. 50,000 registros)
    print("Iniciando descarga de datos desde la API...")
    df_resultado = obtener_datos_cdmx(ID_EJEMPLO, limite=50000)
    
    if not df_resultado.empty:
        # Definir la ruta usando pathlib (Buena práctica para evitar errores en Windows/Mac)
        # Esto apuntará a la carpeta data/raw/ dentro de tu proyecto
        base_dir = Path(__file__).resolve().parent.parent.parent
        raw_dir = base_dir / "data" / "raw"
        
        # Crear las carpetas si no existen
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        # Ruta final del archivo
        archivo_salida = raw_dir / "raw_afluencia_metro.csv"
        
        # Guardar el DataFrame como CSV
        df_resultado.to_csv(archivo_salida, index=False)
        print(f"¡Éxito! Se guardaron {len(df_resultado)} registros en: {archivo_salida}")
    else:
        print("No se pudo descargar la información. Revisa tu conexión o la API.")
