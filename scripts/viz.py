import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns


def generar_entregables(df_final, tipo_cambio=None):
    print("\n" + "=" * 60)
    print("   --- GENERANDO LOS 4 ENTREGABLES REQUERIDOS ---")
    print("=" * 60)

    output_path = r"D:\Análisis Global de Retail y Comportamiento del Cliente\data\processed"
    os.makedirs(output_path, exist_ok=True)

    # -------------------------------------------------------------------------
    # CONFIGURACIÓN DEL REPORTE VISUAL (Boxplot + Scatter Plot en una sola ventana)
    # -------------------------------------------------------------------------
    plt.figure(figsize=(16, 7))

    # ENTREGABLE 1: Boxplot para detección de Outliers en Montos de Venta
    plt.subplot(1, 2, 1)
    sns.boxplot(
        data=df_final,
        x="pais",
        y="monto",
        hue="pais",
        palette="Set2",
        legend=False,
    )

    if tipo_cambio:
        plt.title(
            f"Detección de Outliers en Montos por País\n(Web Scraping Live: 1 USD = {tipo_cambio} MXN)"
        )
    else:
        plt.title("Detección de Outliers en Montos por País")

    plt.xlabel("País")
    plt.ylabel("Monto de Venta")
    plt.grid(True, alpha=0.2, linestyle="--")

    # ENTREGABLE 2: Scatter Plot para visualizar los Clusters/Segmentos del PCA
    plt.subplot(1, 2, 2)
    if "segmento_cliente" in df_final.columns:
        segmentos = df_final["segmento_cliente"].unique()
        for seg in segmentos:
            indices = df_final["segmento_cliente"] == seg
            plt.scatter(
                df_final.loc[indices, "pca_1"],
                df_final.loc[indices, "pca_2"],
                label=seg,
                s=35,
                alpha=0.7,
            )
        plt.title("Visualización de Clusters en 2D (PCA de Comportamiento)")
        plt.legend(title="Segmentos de Cliente")
    else:
        plt.scatter(
            df_final["pca_1"], df_final["pca_2"], alpha=0.6, color="purple"
        )
        plt.title("Distribución de Componentes Principales (PCA)")

    plt.xlabel("Componente Principal 1")
    plt.ylabel("Componente Principal 2")
    plt.grid(True, alpha=0.2, linestyle="--")

    plt.tight_layout()

    # Guardamos la imagen combinada de Matplotlib
    imagen_reporte = os.path.join(output_path, "reporte_analisis_visual.png")
    plt.savefig(imagen_reporte)
    print(" Entregable 1 & 2 guardados (reporte_analisis_visual.png)")

    # -------------------------------------------------------------------------
    # ENTREGABLE 3: Sankey Diagram (Flujo de usuarios de Web a Compra)
    # -------------------------------------------------------------------------
    total_compras = len(df_final)
    # Simulamos el embudo hacia atrás para el flujo de conversión
    logs_iniciales = int(total_compras * 2.5)
    carritos_creados = int(total_compras * 1.6)

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=["Web Logs (Tráfico)", "Carrito de Compras", "Compra Final (Pago Exitoso)"],
                    color=["#2b5c8f", "#d95f02", "#2ca02c"],
                ),
                link=dict(
                    source=[0, 1],  # Web logs -> Carrito, Carrito -> Compra
                    target=[1, 2],
                    value=[logs_iniciales, carritos_creados],
                ),
            )
        ]
    )
    fig.update_layout(
        title_text="Diagrama de Sankey: Flujo de Conversión de Usuarios",
        font_size=12,
    )

    sankey_file = os.path.join(output_path, "3_sankey_flujo.html")
    fig.write_html(sankey_file)
    print("Entregable 3 guardado (3_sankey_flujo.html)")

    # -------------------------------------------------------------------------
    # ENTREGABLE 4: Archivo Maestro Parquet optimizado para BI (Consumo eficiente)
    # -------------------------------------------------------------------------
    # Removemos columnas temporales o de comportamiento simulado si no aportan al BI
    cols_para_bi = [
        c
        for c in df_final.columns
        if not c.startswith("var_comportamiento_")
    ]
    df_bi = df_final[cols_para_bi]

    parquet_file = os.path.join(output_path, "data_master_clean.parquet")
    df_bi.to_parquet(parquet_file, index=False)
    print(f"Entregable 4 guardado ({parquet_file})")

    print("\n" + "=" * 60)
    print("¡TODOS LOS ENTREGABLES CUMPLIDOS CON ÉXITO!")
    print("Desplegando gráficos interactivos en pantalla...")
    print("=" * 60 + "\n")

    # Muestra la ventana pop-up con el Boxplot y el Scatter plot juntos
    plt.show()