import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    # 1. Definir las rutas de entrada y salida de forma segura
    base_dir = Path(__file__).resolve().parent.parent.parent
    raw_file = base_dir / "data" / "raw" / "raw_afluencia_metro.csv"
    processed_dir = base_dir / "data" / "processed"
    processed_file = processed_dir / "clean_afluencia_metro.csv"

    # Crear la carpeta 'processed' si no existe
    processed_dir.mkdir(parents=True, exist_ok=True)

    print(f"Leyendo datos crudos desde: {raw_file}")
    
    # Validar que el archivo crudo exista antes de intentar leerlo
    if not raw_file.exists():
        print("Error: No se encontró el archivo crudo. Ejecuta cdmx_api.py primero.")
        exit()

    # 2. Leer los datos a Pandas (Extract)
    df = pd.read_csv(raw_file)

    print("Iniciando la limpieza de datos (Transform)...")

    # 3. Transformaciones (Limpieza)
    
    # A. Convertir la columna 'fecha' a un tipo de dato Datetime (Tiempo)
    # Esto nos permitirá agrupar por mes, año o día de la semana más adelante
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'])

    # B. Estandarizar textos: quitar espacios al inicio/final y pasar a mayúsculas
    if 'linea' in df.columns:
        df['linea'] = df['linea'].str.strip().str.upper()
    
    if 'estacion' in df.columns:
        df['estacion'] = df['estacion'].str.strip().str.upper()
        # Quitar acentos (ej. convierte "ZÓCALO" a "ZOCALO")
        df['estacion'] = df['estacion'].str.normalize('NFKD')\
                                     .str.encode('ascii', errors='ignore')\
                                     .str.decode('utf-8')

    # C. Limpiar la columna numérica (afluencia)
    if 'afluencia' in df.columns:
        # Convertir a número, si hay algún error (texto basura) lo vuelve NaN (Nulo)
        df['afluencia'] = pd.to_numeric(df['afluencia'], errors='coerce')
        # Rellenar los nulos con 0 y asegurar que sean números enteros
        df['afluencia'] = df['afluencia'].fillna(0).astype(int)

    # D. Eliminar registros exactamente duplicados
    df = df.drop_duplicates()

    # E. (Opcional) Eliminar filas que no tengan estación registrada
    if 'estacion' in df.columns:
        df = df.dropna(subset=['estacion'])

    # 4. Guardar los datos limpios (Load)
    # index=False evita que se guarde una columna extra con el número de fila
    df.to_csv(processed_file, index=False)
    
    print(f"¡Éxito! Datos limpios guardados en: {processed_file}")
    print(f"Total de registros finales: {len(df)}")