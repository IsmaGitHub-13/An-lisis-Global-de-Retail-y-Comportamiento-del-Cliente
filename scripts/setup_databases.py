import psycopg2
from pymongo import MongoClient
import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()
PATH_RAW = "../data/raw/"
if not os.path.exists(PATH_RAW):
    os.makedirs(PATH_RAW)

import psycopg2

def populate_postgres():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="retail_db",
            user="postgres",
            password="130802", 
            client_encoding='utf8' 
        )
        cur = conn.cursor()
        for _ in range(7500):
            cur.execute(
                "INSERT INTO Ventas_historicas (id_cliente, monto, fecha, id_tienda) VALUES (%s, %s, %s, %s)",
                (random.randint(1000, 2500), round(random.uniform(10, 5000), 2), 
                 fake.date_this_year().strftime('%d/%m/%Y'), random.randint(1, 10))
            )
        conn.commit()
        print("SQL listo (7,500 filas).")
    except Exception as e:
        print(f"Error: {e}")

def populate_mongodb():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client['retail_data']
        col = db['perfiles_usuarios']
        col.delete_many({})
        print("Generando 1,500 perfiles en MongoDB...")
        perfiles = []
        for i in range(1000, 2500):
            perfiles.append({
                "id_cliente": i,
                "nombre": fake.name(),
                "edad": random.randint(18, 80),
                "preferencias": random.choice(['Moda', 'Hogar', 'Tecnología']),
                "pais": random.choice(["mx", "México", "MEX", "Mexico"]) # Para limpiar strings
            })
        col.insert_many(perfiles)
        print("MongoDB listo (1,500 docs).")
    except Exception as e: print(f"Error Mongo: {e}")

def create_dirty_inventory():
    print("Generando inventario.csv sucio...")
    base_data = []
    for i in range(800):
        base_data.append({
            'sku_id': f'SKU-{1000+i}',
            'producto': fake.word().upper(),
            'stock': random.randint(1, 1000),
            'costo': round(random.uniform(5, 200), 2)
        })
    df = pd.DataFrame(base_data)
    
    duplicados = df.sample(n=40)
    df = pd.concat([df, duplicados], ignore_index=True)
    
    nulos_indices = df.sample(n=80).index
    df.loc[nulos_indices, 'stock'] = np.nan
    
    df.to_csv(os.path.join(PATH_RAW, "inventario.csv"), index=False)
    print("CSV listo (840 filas con errores).")

def create_server_logs():
    print("Generando logs_servidor.txt...")
    with open(os.path.join(PATH_RAW, "logs_servidor.txt"), "w") as f:
        for _ in range(2500):
            ts = fake.date_time_this_year()
            lvl = random.choice(['INFO', 'ERROR', 'WARN'])
            uid = f"UserID_{random.randint(1000, 2500)}"
            msg = random.choice(["Login", "Logout", "Purchase Error", "Add to Cart"])
            f.write(f"[{ts}] {lvl}: {uid} - {msg}\n")
    print("Logs listos (2,500 líneas).")

if __name__ == "__main__":
    populate_postgres()
    populate_mongodb()
    create_dirty_inventory()
    create_server_logs()
    print("DATOS CREADOS")