from scripts.extraction import extraer_todo
from scripts.transformation import ejecutar_pipeline_etl, obtener_tipo_cambio_live
from scripts.viz import generar_entregables


def run_pipeline():
    # 1. Extracción limpia
    df_v, df_p, df_i = extraer_todo()

    # 2. Obtener el tipo de cambio del scraping para pasarle a la gráfica directamente
    tipo_cambio_actual = obtener_tipo_cambio_live()

    # 3. Pipeline de transformación y análisis
    df_final = ejecutar_pipeline_etl(df_v, df_p, df_i)

    # 4. Generación de entregables con tablas en consola y ventana Pop-up
    generar_entregables(df_final, tipo_cambio=tipo_cambio_actual)


if __name__ == "__main__":
    run_pipeline()