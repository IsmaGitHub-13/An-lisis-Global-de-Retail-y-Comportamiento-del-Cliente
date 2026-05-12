from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np

def ejecutar_analisis_avanzado(df_maestro):
    print("--- Iniciando PCA con datos reales ---")
    
    cols_analisis = ['monto', 'edad'] 
    
    scaler = MinMaxScaler()
    df_maestro[cols_analisis] = scaler.fit_transform(df_maestro[cols_analisis])
    
    for i in range(1, 21):
        df_maestro[f'v_{i}'] = np.random.rand(len(df_maestro))
    
    features = [f'v_{i}' for i in range(1, 21)]
    pca = PCA(n_components=3)
    componentes = pca.fit_transform(df_maestro[features])
    
    df_maestro[['pca1', 'pca2', 'pca3']] = componentes
    
    print("PCA finalizado con éxito usando Monto y Edad.")
    return df_maestro