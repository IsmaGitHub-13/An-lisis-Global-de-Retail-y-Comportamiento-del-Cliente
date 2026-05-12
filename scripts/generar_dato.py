import pandas as pd
import numpy as np
import os

# Configuración de ruta
PATH_RAW = r"D:\Análisis Global de Retail y Comportamiento del Cliente\data\raw"
os.makedirs(PATH_RAW, exist_ok=True)

def crear_inventario_sucio():
    print("Generando inventario con 1,000 filas...")
    np.random.seed(42)
    
    # 1. Crear 1,000 filas base
    data = {
        'id_producto': range(1, 1001),
        'nombre_producto': [f'Producto_{i}' for i in range(1, 1001)],
        'stock': np.random.randint(0, 500, 1000).astype(float),
        'precio': np.random.uniform(10.0, 1000.0, 1000)
    }
    df = pd.DataFrame(data)

    # 2. Insertar 10% de valores nulos (100 filas) en 'stock'
    nulos_idx = np.random.choice(df.index, 100, replace=False)
    df.loc[nulos_idx, 'stock'] = np.nan

    # 3. Insertar 5% de duplicados (50 filas)
    duplicados = df.sample(50)
    df = pd.concat([df, duplicados], ignore_index=True)

    # Guardar
    file_path = os.path.join(PATH_RAW, "inventario.csv")
    df.to_csv(file_path, index=False)
    print(f"Archivo creado en: {file_path}")
    print(f"Filas totales: {len(df)} (incluyendo duplicados)")
    print(f"Nulos en stock: {df['stock'].isna().sum()}")

if __name__ == "__main__":
    crear_inventario_sucio()