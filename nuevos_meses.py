import pandas as pd
import numpy as np
import os
import traceback
import sys
from db_config import get_engine

# Carpeta donde están los nuevos archivos
carpeta = "data_agregar"

dfs = []

print(f"🔍 Buscando nuevos archivos en '{carpeta}'...")

# Usar os.walk para leer archivos recursivamente (incluso en subcarpetas)
for root, dirs, files in os.walk(carpeta):
    for f in files:
        if f.endswith('.xlsx') and not f.startswith('~$'):
            ruta = os.path.join(root, f)
            print(f"  📄 Leyendo: {f}")
            
            try:
                # Leer el archivo Excel
                df = pd.read_excel(ruta)
                
                # Extraer categoría del nombre del archivo (ej: "almacen_enero_2026.xlsx" -> "almacen")
                nombre_base = f.lower().replace('.xlsx', '')
                categoria = nombre_base.split('_')[0] if '_' in nombre_base else nombre_base
                df['Categoria'] = categoria
                
                # Limpieza de datos (igual que en main.py)
                if 'Descuento' in df.columns:
                    df = df.drop(columns=['Descuento'])
                
                df = df.dropna(how='all')
                
                # Filtrar filas de totales (identificando fecha y producto)
                col_fecha = [c for c in df.columns if 'fecha' in str(c).lower()]
                if col_fecha:
                    df = df.dropna(subset=[col_fecha[0]])
                
                col_nombre = [c for c in df.columns if 'nombre' in str(c).lower() or 'producto' in str(c).lower()]
                if col_nombre:
                    df = df.dropna(subset=[col_nombre[0]])
                
                dfs.append(df)
            except Exception as e:
                print(f"  ❌ Error procesando {f}: {e}")

if not dfs:
    print("⚠️ No se encontraron archivos nuevos válidos en 'data_agregar'.")
    sys.exit()

# Parte 2: Unificar y Normalizar
df_unificado = pd.concat(dfs, ignore_index=True)

# Normalizar nombres de columnas
df_unificado.columns = df_unificado.columns.str.lower().str.strip().str.replace(" ", "_").str.replace(".", "", regex=False)

# Eliminar duplicados de columnas (evita el error de 'fecha is already present')
df_unificado = df_unificado.loc[:, ~df_unificado.columns.duplicated()]

# Asegurar formato de fecha
if 'fecha' in df_unificado.columns:
    df_unificado['fecha'] = pd.to_datetime(df_unificado['fecha'], errors='coerce')
    df_unificado = df_unificado.dropna(subset=['fecha'])

# Parte 3: Conexión y carga a PostgreSQL (Modo APPEND)
try:
    from sqlalchemy import text # Asegurar que text esté disponible
    engine = get_engine()

    print(f"\n📤 Cargando {len(df_unificado)} registros nuevos en la tabla 'ventas'...")
    
    # IMPORTANTE: Usamos if_exists='append' para sumar a lo que ya existe en la DB
    df_unificado.to_sql(
        'ventas',
        engine,
        schema='public',
        if_exists='append',
        index=False,
        chunksize=1000,
        method='multi'
    )

    with engine.connect() as connection:
        count = connection.execute(text("SELECT COUNT(*) FROM public.ventas")).fetchone()[0]
        print(f"✅ ¡PROCESO EXITOSO! Total actual en la base de datos: {count} registros.")

except Exception as e:
    print("\n❌ ERROR AL CARGAR DATOS EN POSTGRESQL")
    print("-" * 60)
    print(str(e))
