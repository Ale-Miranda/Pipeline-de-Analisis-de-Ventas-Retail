import pandas as pd
from sqlalchemy import text
import sys
from db_config import get_engine

def check_db():
    try:
        engine = get_engine()
        
        with engine.connect() as conn:
            # 1. Conteo total
            total = conn.execute(text("SELECT COUNT(*) FROM ventas")).scalar()
            
            # 2. Conteo por categoría
            result_cat = conn.execute(text("SELECT categoria, COUNT(*) as registros FROM ventas GROUP BY categoria ORDER BY registros DESC"))
            info_cat = result_cat.fetchall()
            
            # 3. Rango de fechas
            result_date = conn.execute(text("SELECT MIN(fecha), MAX(fecha) FROM ventas"))
            min_f, max_f = result_date.fetchone()
            
            # 4. Registros por mes (para ver si se cargó 2026)
            result_mes = conn.execute(text("""
                SELECT TO_CHAR(fecha, 'YYYY-MM') as mes, COUNT(*) as cantidad 
                FROM ventas 
                GROUP BY mes 
                ORDER BY mes DESC
            """))
            info_mes = result_mes.fetchall()

        print(f"\n--- ESTADO DE LA BASE DE DATOS VENTAS (PostgreSQL) ---")
        print(f"Total de registros: {total}")
        print(f"Rango de fechas: desde {min_f} hasta {max_f}")
        
        print("\n--- REGISTROS POR MES ---")
        for mes, cant in info_mes:
            print(f"  {mes}: {cant} registros")
            
        print("\n--- REGISTROS POR CATEGORÍA ---")
        for cat, cant in info_cat:
            print(f"  {cat}: {cant}")
            
    except Exception as e:
        print(f"Error al verificar la base de datos: {e}")

if __name__ == "__main__":
    check_db()
