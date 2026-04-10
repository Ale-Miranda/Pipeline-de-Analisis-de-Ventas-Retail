--Queries para analizar los datos de ventas

--ventas totales
SELECT SUM(subtotal) AS ventas_totales
FROM ventas;

--venta promedio
SeLECT AVG(subtotal) AS venta_promedio
FROM ventas;

--ventas por categoria
SELECT 
    categoria, 
    SUM(subtotal) AS ventas_categoria,
    COUNT(*) AS cantidad_ventas
FROM ventas
GROUP BY categoria
ORDER BY ventas_categoria DESC; 

--Top 10 productos más vendidos
SELECT "Nombre del Producto", SUM(Subtotal) AS total_vendido  
FROM ventas
GROUP BY "Nombre del Producto"
ORDER BY total_vendido DESC
LIMIT 10;

--productos menos vendidos
SELECT 
    "Nombre del Producto",
    SUM(Subtotal) AS total_vendido
FROM ventas
GROUP BY "Nombre del Producto"
HAVING SUM(cantidad) < 10
ORDER BY total_vendido
limit 50;

--venta por mes
SELECT 
    strftime('%Y-%m', fecha) AS mes,
    SUM(subtotal) AS ventas_mensuales
FROM ventas
GROUP BY mes
ORDER BY mes;

--mes con mas ventas
SELECT 
    strftime('%Y-%m', fecha) AS mes,
    SUM(subtotal) AS ventas_mensuales
FROM ventas
GROUP BY mes
ORDER BY ventas_mensuales DESC
LIMIT 1; 

--mes con menos ventas
SELECT 
    strftime('%Y-%m', fecha) AS mes,
    SUM(subtotal) AS ventas_mensuales
FROM ventas
GROUP BY mes
ORDER BY ventas_mensuales ASC
LIMIT 1; 

--margen de ganancia promedio por categoria en porcentaje
SELECT 
    categoria,
    AVG(Ganancia/subtotal) * 100 AS margen_promedio_porcentaje
FROM ventas
GROUP BY categoria
ORDER BY margen_promedio_porcentaje DESC;