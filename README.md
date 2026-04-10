# 📊 Pipeline de Análisis de Ventas Retail
> **Proyecto End-to-End: Automatización de Ingesta, Limpieza y Visualización de Datos.**

Este proyecto resuelve el desafío de consolidar datos de ventas dispersos en múltiples archivos Excel para un negocio minorista, transformándolos en una base de datos relacional y un dashboard interactivo para la toma de decisiones.

---

## 🧭 Escenario de Negocio
Un negocio con múltiples rubros (Almacén, Bebidas, Lácteos, etc.) genera reportes mensuales independientes. La falta de consolidación impedía identificar rápidamente productos rentables, tendencias mensuales y márgenes por categoría.

### Solución:
Un pipeline automatizado en Python que extrae, limpia, normaliza y carga los datos en **PostgreSQL**, permitiendo un análisis SQL profundo y visualización en **Power BI**.

---

## 🛠️ Stack Tecnológico
| Capa | Tecnología |
| :--- | :--- |
| **Lenguaje** | Python 3.13 |
| **Librerías** | Pandas, NumPy, SQLAlchemy |
| **Base de Datos** | PostgreSQL (Docker/Local) |
| **Visualización** | Power BI |
| **Entorno** | .env para gestión de credenciales |

---

## 📐 Arquitectura del Pipeline

```mermaid
graph LR
    A[Excel crudos] --> B[Python / Pandas]
    B --> C{Limpieza y <br/> Normalización}
    C --> D[(PostgreSQL)]
    D --> E[Vistas SQL Análiticas]
    E --> F[Dashboard Power BI]
```

---

## ⚙️ Componentes del Proyecto

1.  **`main.py`**: Motor de ingesta masiva. Lee los archivos de la carpeta `data/`, normaliza nombres de columnas y carga la tabla maestra en SQL.
2.  **`nuevos_meses.py`**: Gestión incremental. Permite añadir nuevos meses de datos a la base de datos existente.
3.  **`db_config.py`**: Centraliza la conexión a la base de datos usando variables de entorno (.env).
4.  **`sql/views.sql`**: Implementación de un modelo dimensional básico para optimizar el dashboard.

---

## 🚀 Cómo empezar

### 1. Requisitos
- Python 3.10+
- PostgreSQL
- `pip install -r requirements.txt` (o instale `pandas`, `sqlalchemy`, `python-dotenv`, `openpyxl`)

### 2. Configuración
Crea un archivo `.env` basado en `.env.example` con tus credenciales de base de datos local:
```env
DB_USER=tu_usuario
DB_PASS=tu_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ventas_db
```

### 3. Ejecución
Para cargar los datos en la base de datos:
```bash
python main.py
```

---

## 📊 Visualización
El dashboard se encuentra en la carpeta `/dashboard`. 
- Dashboard general
![Dashboard general](dashboard/_dashboard_general.png)
![Dashboard general](dashboard/_dashboard_general_2.png)
- Dashboard productos
![Dashboard productos](dashboard/_dashboard_productos.png)
![Dashboard productos](dashboard/_dashboard_productos_2.png)

*(Nota: Para abrirlo correctamente en otra PC, asegúrate de actualizar el origen de datos en Power BI para que apunte a tu instancia local de PostgreSQL).*

---

## 💡 Impacto y Aprendizajes
- **Reducción de tiempo**: Procesos que tomaban horas de consolidación manual ahora se ejecutan en segundos.
* **Integridad del dato**: Eliminación de errores humanos mediante limpieza automatizada.
* **Escalabilidad**: El sistema está preparado para crecer con el negocio mes a mes.

---
*Desarrollado como proyecto de portafolio para demostrar habilidades en Data Engineering y BI.*
