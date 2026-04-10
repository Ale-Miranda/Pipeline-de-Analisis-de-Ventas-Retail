-- =====================================
-- DIMENSION: PRODUCTO
-- =====================================

CREATE OR REPLACE VIEW dim_producto AS
SELECT DISTINCT
    nombre_del_producto
FROM ventas
WHERE nombre_del_producto IS NOT NULL;


-- =====================================
-- DIMENSION: CATEGORIA
-- =====================================

CREATE OR REPLACE VIEW dim_categoria AS
SELECT DISTINCT
    categoria
FROM ventas
WHERE categoria IS NOT NULL;


-- =====================================
-- DIMENSION: FECHA
-- =====================================

CREATE OR REPLACE VIEW dim_fecha AS
SELECT DISTINCT
    fecha::date AS fecha,
    EXTRACT(DAY FROM fecha) AS dia,
    EXTRACT(MONTH FROM fecha) AS mes,
    EXTRACT(YEAR FROM fecha) AS anio,
    TO_CHAR(fecha, 'Month') AS nombre_mes
FROM ventas
WHERE fecha IS NOT NULL;


-- =====================================
-- TABLA DE HECHOS
-- =====================================

CREATE OR REPLACE VIEW fact_ventas AS
SELECT 
    fecha::date AS fecha,
    nombre_del_producto,
    categoria,
    cantidad,
    precio_un,
    subtotal,
    ganancia
FROM ventas;


CREATE OR REPLACE VIEW ventas_mensuales AS
SELECT 
    DATE_TRUNC('month', fecha) AS mes,
    SUM(subtotal) AS ventas,
    SUM(ganancia) AS ganancia,
    SUM(cantidad) AS unidades
FROM ventas
GROUP BY mes
ORDER BY mes;