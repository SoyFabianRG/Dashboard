import requests
import pandas as pd

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
    # --- PRUEBA DEL SCRIPT ---
    # Ejemplo: Afluencia diaria del Metro CDMX
    # URL original: https://datos.cdmx.gob.mx/dataset/afluencia-diaria-del-metro-cdmx/resource/cce544e1-dc6b-42b4-bc27-0d8e6eb3ed72
    ID_EJEMPLO = "cce544e1-dc6b-42b4-bc27-0d8e6eb3ed72"
    
    df_resultado = obtener_datos_cdmx(ID_EJEMPLO, limite=5)
    
    print("\n--- Vista Previa de Datos ---")
    print(df_resultado.head())
    print("\n--- Columnas Disponibles ---")
    print(df_resultado.columns.tolist())
