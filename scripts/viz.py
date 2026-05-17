import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import pandas as pd
import os

def generar_entregables(df_final):
    print("--- Generando Entregables Finales ---")
    output_path = r"D:\Análisis Global de Retail y Comportamiento del Cliente\data\processed"
    os.makedirs(output_path, exist_ok=True)

    # --------------------------------------------------
    # 1. GRÁFICO DE BARRAS: Monto Promedio por País
    # --------------------------------------------------
    plt.figure(figsize=(10, 6))
    # Agrupamos los datos para obtener el promedio por país
    df_monto_pais = df_final.groupby('pais')['monto'].mean().reset_index()
    
    sns.barplot(data=df_monto_pais, x='pais', y='monto', palette='Blues_d')
    plt.title("Monto Promedio de Venta por País")
    plt.xlabel("País")
    plt.ylabel("Monto Promedio")
    plt.xticks(rotation=45) # Rota los nombres si son largos
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "1_barras_montos.png"))
    plt.close()

    # --------------------------------------------------
    # 2. GRÁFICO DE BARRAS: Conteo de Clientes por País
    # --------------------------------------------------
    plt.figure(figsize=(10, 6))
    # Contamos cuántos registros/clientes hay por cada país
    sns.countplot(data=df_final, x='pais', palette='viridis', order=df_final['pais'].value_counts().index)
    plt.title("Distribución / Conteo de Clientes por País")
    plt.xlabel("País")
    plt.ylabel("Cantidad de Clientes")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "2_barras_conteo_pais.png"))
    plt.close()

    # 3. DIAGRAMA DE SANKEY (Se mantiene igual)
    fig = go.Figure(data=[go.Sankey(
        node = dict(pad = 15, thickness = 20, line = dict(color = "black", width = 0.5),
          label = ["Web Log", "Carrito de Compras", "Pago Exitoso"],
          color = "blue"),
        link = dict(
          source = [0, 1], 
          target = [1, 2], 
          value = [len(df_final)*1.5, len(df_final)] 
      ))])
    fig.update_layout(title_text="Flujo de Conversión de Usuarios", font_size=10)
    fig.write_html(os.path.join(output_path, "3_sankey_flujo.html"))

    # 4. GUARDAR PARQUET (Se mantiene igual)
    df_final.to_parquet(os.path.join(output_path, "data_master_clean.parquet"), index=False)
    
    print(f" Todos los archivos guardados en: {output_path}")