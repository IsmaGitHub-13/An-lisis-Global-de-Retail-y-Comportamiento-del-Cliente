from scripts.extraction import extraer_todo
from scripts.cleaning import limpiar_datos
from scripts.analysis import ejecutar_analisis_avanzado
from scripts.viz import generar_entregables

def run_pipeline():
    # Extracción de SQL, Mongo y CSV
    df_v, df_p, df_i = extraer_todo()
    
    # Limpieza de nulos y duplicados
    df_v, df_p, df_i = limpiar_datos(df_v, df_p, df_i)
    
    # Unión de bases de datos
    df_maestro = df_v.merge(df_p, on='id_cliente', how='inner')
    
    # Análisis: MinMaxScaler + PCA
    df_final = ejecutar_analisis_avanzado(df_maestro)
    
    # Generación de los 4 entregables
    generar_entregables(df_final)

if __name__ == "__main__":
    run_pipeline()