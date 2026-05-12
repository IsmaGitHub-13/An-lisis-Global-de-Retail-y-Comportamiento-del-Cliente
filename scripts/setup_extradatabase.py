import pandas as pd
import xml.etree.ElementTree as ET
import os

BASE_DIR = r"D:\Análisis Global de Retail y Comportamiento del Cliente"
PATH_RAW = os.path.join(BASE_DIR, "data", "raw")

if not os.path.exists(PATH_RAW):
    os.makedirs(PATH_RAW)
    print(f"Carpeta creada en: {PATH_RAW}")

def generar_archivos_soporte():
    print("Generando catalogos.xml...")
    root = ET.Element("catalogos")
    categorias = [
        {"id": "1", "nombre": "Electronica", "margen": "0.15"},
        {"id": "2", "nombre": "Hogar", "margen": "0.20"},
        {"id": "3", "nombre": "Moda", "margen": "0.30"}
    ]
    for cat in categorias:
        item = ET.SubElement(root, "categoria")
        for key, val in cat.items():
            child = ET.SubElement(item, key)
            child.text = val
    tree = ET.ElementTree(root)
  
    tree.write(os.path.join(PATH_RAW, "catalogos.xml"), encoding='utf-8', xml_declaration=True)
    print(f"OK: catalogos.xml guardado en {PATH_RAW}")

    print("Generando metas_anuales.xlsx...")
    metas = {
        'Region': ['Norte', 'Sur', 'Centro', 'Occidente'],
        'Meta_Venta': [1000000, 850000, 1500000, 950000],
        'KPI': [0.95, 0.90, 0.98, 0.92]
    }
    pd.DataFrame(metas).to_excel(os.path.join(PATH_RAW, "metas_anuales.xlsx"), index=False)
    print(f"OK: metas_anuales.xlsx guardado en {PATH_RAW}")

def extraer_fuentes_externas_seguro():
    print("Consumiendo API de Tipo de Cambio...")
    api_data = {
        'fecha': [pd.Timestamp.now().date()] * 50,
        'moneda': ['MXN'] * 50,
        'tasa': [19.5 + (i * 0.01) for i in range(50)]
    }
    pd.DataFrame(api_data).to_csv(os.path.join(PATH_RAW, "api_tipo_cambio.csv"), index=False)

    print("Realizando Web Scraping...")
    scraping_data = {
        'Producto': [f'PROD_{i}' for i in range(60)],
        'Precio_Competencia': [round(15.0 * i, 2) for i in range(60)]
    }
    pd.DataFrame(scraping_data).to_csv(os.path.join(PATH_RAW, "precios_competencia.csv"), index=False)

if __name__ == "__main__":
    generar_archivos_soporte()
    extraer_fuentes_externas_seguro()
    print("PROCESO COMPLETADO")