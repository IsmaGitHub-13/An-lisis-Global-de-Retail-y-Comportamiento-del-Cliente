import pandas as pd
import psycopg2
from pymongo import MongoClient
import os

BASE_DIR = r"D:\Análisis Global de Retail y Comportamiento del Cliente"
PATH_RAW = os.path.join(BASE_DIR, "data", "raw")

def extraer_todo():
    print("Iniciando Fase de Extracción...")
    
    # SQL - Ventas
    conn = psycopg2.connect(host="localhost", database="retail_db", user="postgres", password="130802")
    df_ventas = pd.read_sql("SELECT * FROM ventas_historicas", conn)
    conn.close()

    # MongoDB - Perfiles
    client = MongoClient("mongodb://localhost:27017/")
    df_perfiles = pd.DataFrame(list(client['retail_data']['perfiles_usuarios'].find()))
    if '_id' in df_perfiles.columns: df_perfiles.drop(columns=['_id'], inplace=True)

    # Archivos Locales
    df_inv = pd.read_csv(os.path.join(PATH_RAW, "inventario.csv"))
    
    print(f"Extracción completada: {len(df_ventas)} ventas cargadas.")
    return df_ventas, df_perfiles, df_inv