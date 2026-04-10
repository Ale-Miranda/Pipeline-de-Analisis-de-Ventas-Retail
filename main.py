import pandas as pd
import numpy as np
import os
import sys
import random
from sqlalchemy import text
from db_config import get_engine

#configuracion
CARPETA_DATOS = "data" 
TABLA_SQL = "ventas"

#anonimizacion de datos
MODO_ANONIMO = True 

def imprimir_banner():
    print("\n" + "="*60)
    print(" INGESTA Y CARGA DE VENTAS ".center(60))
    if MODO_ANONIMO:
        print(" *** MODO RUIDO PROFUNDO ACTIVADO *** ".center(60))
    print("="*60)

def procesar_archivos():
    """Lee y limpia los archivos Excel de la carpeta data/."""
    if not os.path.exists(CARPETA_DATOS):
        print(f"ERROR: La carpeta '{CARPETA_DATOS}' no existe.")
        return None

    archivos = [
        f for f in os.listdir(CARPETA_DATOS) 
        if f.endswith('.xlsx') and not f.startswith('~$') and f != 'ventas_unificado.xlsx'
    ]
    
    if not archivos:
        print(f"AVISO: No se encontraron archivos válidos en '{CARPETA_DATOS}'.")
        return None

    print(f"Procesando {len(archivos)} archivos...")
    dfs = []
    
    for archivo in archivos:
        ruta = os.path.join(CARPETA_DATOS, archivo)
        try:
            df = pd.read_excel(ruta)
            categoria = archivo.split('_')[0].split('20')[0].replace('.xlsx','').lower().strip()
            df['Categoria'] = categoria
            
            if 'Descuento' in df.columns:
                df = df.drop(columns=['Descuento'])
            
            df = df.dropna(how='all')
            
            # filtro de filas válidas
            col_fecha = [c for c in df.columns if 'fecha' in str(c).lower()]
            if col_fecha:
                df = df.dropna(subset=[col_fecha[0]])
            
            col_nombre = [c for c in df.columns if 'nombre' in str(c).lower() or 'producto' in str(c).lower()]
            if col_nombre:
                df = df.dropna(subset=[col_nombre[0]])
            
            dfs.append(df)
            print(f"  -> {archivo}: {len(df)} registros.")
        except Exception as e:
            print(f"  Error en {archivo}: {e}")

    if not dfs: return None

    df_unificado = pd.concat(dfs, ignore_index=True)
    df_unificado.columns = df_unificado.columns.str.lower().str.strip().str.replace(" ", "_").str.replace(".", "", regex=False)
    df_unificado = df_unificado.loc[:, ~df_unificado.columns.duplicated()]
    
    return df_unificado

def aplicar_ruido_profundo(df):
    """Aplica ruido aleatorio agresivo e irreversible por cada fila."""
    print("\nAlicando RUIDO PROFUNDO a precios y ganancias...")
    
    # Me aseguro que las columnas existen y son numéricas
    for col in ['precio_un', 'ganancia', 'cantidad', 'subtotal']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 1. Genero factores aleatorios distintos para cada registro (entre 0.4 y 1.5)
    factores_precio = [random.uniform(0.4, 1.5) for _ in range(len(df))]
    factores_margen = [random.uniform(0.6, 1.4) for _ in range(len(df))]

    # 2. Altero precios de forma irreversible
    df['precio_un'] = (df['precio_un'] * factores_precio).round(2)
    
    # 3. Recalculo subtotal para mantener coherencia en el Dashboard
    df['subtotal'] = (df['precio_un'] * df['cantidad']).round(2)
    
    # 4. Alterar Ganancia (usando un segundo factor para que no sea proporcional al precio)
    df['ganancia'] = (df['ganancia'] * factores_margen).round(2)

    print("OK - Datos anonimizados de forma irreversible.")
    return df

def cargar_a_db(df):
    """Carga el DataFrame en PostgreSQL."""
    try:
        engine = get_engine()
        print("\nLimpiando base de datos (DROP CASCADE)...")
        with engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT").execute(text(f"DROP TABLE IF EXISTS {TABLA_SQL} CASCADE"))

        print(f"Cargando {len(df)} registros en la tabla '{TABLA_SQL}'...")
        df.to_sql(TABLA_SQL, engine, index=False, if_exists='replace', chunksize=1000, method='multi')
        return True
    except Exception as e:
        print(f"Error en la carga SQL: {e}")
        return False

def recrear_vistas():
    """Restaura el modelo dimensional."""
    print("\nRestaurando vistas analíticas...")
    try:
        engine = get_engine()
        with open('views.sql', 'r', encoding='utf-8') as f:
            sqls = f.read().split(';')
            with engine.connect() as conn:
                conn.execution_options(isolation_level="AUTOCOMMIT")
                for sql in sqls:
                    if sql.strip():
                        conn.execute(text(sql))
        print("Hecho.")
        return True
    except Exception as e:
        print(f"Error al recrear vistas: {e}")
        return False

def main():
    imprimir_banner()
    
    # 1. Ingesta
    df = procesar_archivos()
    if df is None: return

    # 2. Aplicar Ruido si está activo
    if MODO_ANONIMO:
        df = aplicar_ruido_profundo(df)

    # 3. Carga y Vistas
    if cargar_a_db(df):
        recrear_vistas()
        print("\n" + "="*60)
        print(" PROCESO COMPLETADO EXITOSAMENTE ".center(60))
        print("="*60 + "\n")

if __name__ == "__main__":
    main()
