import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

BASE_DIR = r"D:\Análisis Global de Retail y Comportamiento del Cliente"
PATH_RAW = os.path.join(BASE_DIR, "data", "raw")
PATH_PROCESSED = os.path.join(BASE_DIR, "data", "processed")

def ejecutar_pipeline_etl(df_ventas, df_perfiles, df_inv):
    print("Iniciando Pipeline de Transformación")
    df_inv['stock'] = df_inv['stock'].fillna(0)
    df_ventas = df_ventas.drop_duplicates()
    print("1. Limpieza: Nulos de inventario e imputados y duplicados de SQL eliminados.")
    
    df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'], dayfirst=True)
    
    scaler = MinMaxScaler()
    cols_a_escalar = ['ingresos', 'gastos_mensuales', 'puntos_lealtad']
    df_perfiles[cols_a_escalar] = scaler.fit_transform(df_perfiles[cols_a_escalar])
    print("2. Normalización: Fechas convertidas y variables escaladas con Min-Max.")
    
    df_maestro = pd.merge(df_ventas, df_perfiles, on='id_cliente', how='left')
    print(f"3. Enriquecimiento: Join completado. Tamaño del dataset: {df_maestro.shape}")
    df_maestro['segmento_cliente'] = np.where(
        (df_maestro['gastos_mensuales'] > 0.7) & (df_maestro['edad'] < 30), 
        "Premium Joven", 
        "Estándar"
    )
    print("4. Reglas de Negocio: Columna 'segmento_cliente' creada.")
    for i in range(1, 21):
        df_maestro[f'var_comportamiento_{i}'] = np.random.rand(len(df_maestro))
    
    features_pca = [f'var_comportamiento_{i}' for i in range(1, 21)]
    pca = PCA(n_components=3)
    componentes = pca.fit_transform(df_maestro[features_pca])
    
    df_maestro['pca_1'] = componentes[:, 0]
    df_maestro['pca_2'] = componentes[:, 1]
    df_maestro['pca_3'] = componentes[:, 2]
    print("5. PCA: Reducción a 3 componentes principales completada.")
    os.makedirs(PATH_PROCESSED, exist_ok=True)
    df_maestro.to_parquet(os.path.join(PATH_PROCESSED, "data_master_clean.parquet"))
    print(f"Archivo final guardado en: {PATH_PROCESSED}")
    
    return df_maestro
if __name__ == "__main__":
    print("Ejecuta este script desde tu main.py o integra las funciones de extracción.")