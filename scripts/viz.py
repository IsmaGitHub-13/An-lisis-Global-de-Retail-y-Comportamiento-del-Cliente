import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import pandas as pd
import os

def generar_entregables(df_final):
    print("--- Generando Entregables Finales ---")
    output_path = r"D:\Análisis Global de Retail y Comportamiento del Cliente\data\processed"
    os.makedirs(output_path, exist_ok=True)

    # 1. BOXPLOT (Detección de Outliers)
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df_final, y='monto', color='skyblue')
    plt.title("Detección de Outliers en Montos de Venta")
    plt.savefig(os.path.join(output_path, "1_boxplot_outliers.png"))
    plt.close()

    # 2. SCATTER PLOT (Clusters tras PCA)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df_final, x='pca1', y='pca2', hue='pais', palette='viridis')
    plt.title("Segmentación de Clientes tras PCA")
    plt.savefig(os.path.join(output_path, "2_scatter_pca.png"))
    plt.close()

    # 3. SANKEY DIAGRAM (Flujo de Usuario)
    # Simulamos el flujo: Web -> Carrito -> Compra
    fig = go.Figure(data=[go.Sankey(
        node = dict(pad = 15, thickness = 20, line = dict(color = "black", width = 0.5),
          label = ["Web Log", "Carrito de Compras", "Pago Exitoso"],
          color = "blue"),
        link = dict(
          source = [0, 1], # indices de origen
          target = [1, 2], # indices de destino
          value = [len(df_final)*1.5, len(df_final)] # flujo simulado
      ))])
    fig.update_layout(title_text="Flujo de Conversión de Usuarios", font_size=10)
    fig.write_html(os.path.join(output_path, "3_sankey_flujo.html"))

    # 4. ARCHIVO FINAL OPTIMIZADO (.parquet)
    df_final.to_parquet(os.path.join(output_path, "data_master_clean.parquet"), index=False)
    
    print(f" Todos los archivos guardados en: {output_path}")