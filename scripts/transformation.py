import os
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

BASE_DIR = r"D:\Análisis Global de Retail y Comportamiento del Cliente"
PATH_PROCESSED = os.path.join(BASE_DIR, "data", "processed")


def obtener_tipo_cambio_live():
    print("Iniciando Web Scraping (Tipo de Cambio)...")
    url = "https://www.google.com/search?q=USD+to+MXN"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            elemento = soup.find(
                "span", {"class": "DFlfde", "data-precision": True}
            )
            if elemento:
                factor = float(elemento["data-value"])
                print(f"[Web Scraping] Éxito! 1 USD = {factor} MXN")
                return factor

        print(
            "No se encontró la etiqueta en la web. Usando valor seguro (18.50 MXN)"
        )
        return 18.50
    except Exception as e:
        print(
            f"Error en Web Scraping: {e}. Usando valor seguro (18.50 MXN)"
        )
        return 18.50


def ejecutar_pipeline_etl(df_ventas, df_perfiles, df_inv):
    print("\n--- Iniciando Pipeline de Transformación y Análisis ---")

    # 1. Limpieza base
    df_inv["stock"] = df_inv["stock"].fillna(0)
    df_ventas = df_ventas.drop_duplicates()
    print(
        "1. Limpieza: Nulos de inventario e imputados y duplicados de SQL eliminados."
    )

    df_ventas["fecha"] = pd.to_datetime(df_ventas["fecha"], dayfirst=True)

    # 2. Obtener tipo de cambio del Web Scraping
    tipo_cambio = obtener_tipo_cambio_live()

    # 3. Enriquecimiento / Cruce de datos (Hacemos el merge PRIMERO)
    df_maestro = pd.merge(df_ventas, df_perfiles, on="id_cliente", how="left")
    print(
        f"2. Enriquecimiento: Join completado. Tamaño del dataset: {df_maestro.shape}"
    )

    # Aplicamos la transformación del tipo de cambio si existe la columna de ingresos
    if "ingresos" in df_maestro.columns:
        df_maestro["ingresos_normalizados_mxn"] = (
            df_maestro["ingresos"] * tipo_cambio
        )

    # 4. Normalización / Escalado (Verificamos cuáles columnas existen realmente)
    scaler = MinMaxScaler()
    cols_a_escalar = ["ingresos", "gastos_mensuales", "puntos_lealtad"]

    # Filtramos solo las columnas que de verdad existan en el set de datos para evitar KeyErrors
    cols_existentes = [c for c in cols_a_escalar if c in df_maestro.columns]

    if cols_existentes:
        # Llenamos nulos con 0 por si acaso el join de MongoDB trajo vacíos
        df_maestro[cols_existentes] = df_maestro[cols_existentes].fillna(0)
        df_maestro[cols_existentes] = scaler.fit_transform(
            df_maestro[cols_existentes]
        )
        print(
            f"3. Normalización: Variables escaladas con Min-Max: {cols_existentes}"
        )
    else:
        print(
            "Advertencia: No se encontraron las columnas de ingresos/gastos para escalar. Saltando Min-Max."
        )

    # 5. Reglas de Negocio
    # Si 'gastos_mensuales' no está, usamos una alternativa segura para que no falle
    if "gastos_mensuales" in df_maestro.columns and "edad" in df_maestro.columns:
        df_maestro["segmento_cliente"] = np.where(
            (df_maestro["gastos_mensuales"] > 0.7) & (df_maestro["edad"] < 30),
            "Premium Joven",
            "Estándar",
        )
    else:
        df_maestro["segmento_cliente"] = "Estándar"
    print("4. Reglas de Negocio: Columna 'segmento_cliente' creada.")

    # 6. Generación de variables de comportamiento simuladas para el PCA
    for i in range(1, 21):
        df_maestro[f"var_comportamiento_{i}"] = np.random.rand(len(df_maestro))

    # 7. Reducción de Dimensionalidad Avanzada (PCA)
    features_pca = [f"var_comportamiento_{i}" for i in range(1, 21)]
    pca = PCA(n_components=3)
    componentes = pca.fit_transform(df_maestro[features_pca])

    df_maestro["pca_1"] = componentes[:, 0]
    df_maestro["pca_2"] = componentes[:, 1]
    df_maestro["pca_3"] = componentes[:, 2]
    print("5. PCA: Reducción a 3 componentes principales completada.")

    # 8. Almacenamiento final
    os.makedirs(PATH_PROCESSED, exist_ok=True)
    df_maestro.to_parquet(
        os.path.join(PATH_PROCESSED, "data_master_clean.parquet")
    )
    print(f"Archivo final maestro guardado en: {PATH_PROCESSED}")

    return df_maestro