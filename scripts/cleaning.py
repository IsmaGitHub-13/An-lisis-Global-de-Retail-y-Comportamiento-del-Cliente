import pandas as pd

def limpiar_datos(df_ventas, df_perfiles, df_inv):
    print("Corrigiendo formato de fechas y limpiando datos...")
    
    # 1. Convertir Timestamp de milisegundos a fecha legible
    # El unit='ms' es la clave para esos números largos
    df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'], unit='ms', errors='coerce')
    
    # 2. Formatear para que solo quede la fecha (sin la hora 00:00:00)
    df_ventas['fecha'] = df_ventas['fecha'].dt.date
    
    # 3. El resto de la limpieza que ya tenías
    df_inv = df_inv.drop_duplicates()
    df_inv['stock'] = df_inv['stock'].fillna(0)
    
    if 'país' in df_perfiles.columns:
        df_perfiles['país'] = df_perfiles['país'].str.strip().str.title()

    print(f"Fecha corregida. Ejemplo: {df_ventas['fecha'].iloc[0]}")
    return df_ventas, df_perfiles, df_inv