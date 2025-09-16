SET search_path TO btg_schema;

-- Opción 1: INNER JOINs anidados (más legible)
SELECT DISTINCT 
    c.nombre,
    c.apellidos,
    c.ciudad
FROM cliente c
INNER JOIN inscripcion i ON c.id = i.idCliente AND i.estado = 'ACTIVA'
INNER JOIN (
    SELECT DISTINCT d.idProducto, d.idSucursal
    FROM disponibilidad d
    INNER JOIN visitan v ON d.idSucursal = v.idSucursal
) productos_visitados ON i.idProducto = productos_visitados.idProducto
WHERE NOT EXISTS (
    SELECT 1
    FROM disponibilidad d2
    INNER JOIN sucursal s ON d2.idSucursal = s.id
    WHERE d2.idProducto = i.idProducto
    AND s.id NOT IN (
        SELECT v2.idSucursal
        FROM visitan v2
        WHERE v2.idCliente = c.id
    )
)
ORDER BY c.nombre, c.apellidos;
