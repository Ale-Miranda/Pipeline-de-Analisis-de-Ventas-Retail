"""
db_config.py
------------
Módulo de infraestructura para la gestión segura de la conexión a la base de datos.
Utiliza variables de entorno para evitar la exposición de credenciales sensibles.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar configuración desde el archivo .env
load_dotenv()

def get_db_url(dbname_override=None):
    """
    Construye la cadena de conexión para PostgreSQL usando las variables de entorno.
    
    Args:
        dbname_override (str, optional): Nombre de DB alternativo (ej: 'postgres' para tareas admin).
    """
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    # Si no se especifica override, toma la DB por defecto del .env
    name = dbname_override if dbname_override else os.getenv("DB_NAME")
    
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"

def get_engine(dbname_override=None):
    """
    Inicializa y retorna un motor de SQLAlchemy configurado.
    """
    url = get_db_url(dbname_override)
    return create_engine(url)
