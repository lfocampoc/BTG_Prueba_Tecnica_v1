SET search_path TO btg_schema;

TRUNCATE TABLE visitan RESTART IDENTITY CASCADE;
TRUNCATE TABLE disponibilidad RESTART IDENTITY CASCADE;
TRUNCATE TABLE inscripcion RESTART IDENTITY CASCADE;
TRUNCATE TABLE sucursal RESTART IDENTITY CASCADE;
TRUNCATE TABLE producto RESTART IDENTITY CASCADE;
TRUNCATE TABLE cliente RESTART IDENTITY CASCADE;

INSERT INTO cliente (nombre, apellidos, ciudad) VALUES
('Juan', 'Pérez', 'Bogotá'),
('María', 'López', 'Medellín'),
('Carlos', 'González', 'Cali'),
('Ana', 'Fernández', 'Bogotá'),
('Luis', 'Martín', 'Barranquilla');

INSERT INTO producto (nombre, tipoProducto) VALUES
('Fondo Conservador', 'FIC'),
('Fondo de Pensiones', 'FPV'),
('Fondo de Acciones', 'FIC'),
('Fondo Mixto', 'FIC'),
('Fondo de Renta Fija', 'FIC');

INSERT INTO sucursal (nombre, ciudad) VALUES
('BTG Centro', 'Bogotá'),
('BTG Norte', 'Bogotá'),
('BTG El Poblado', 'Medellín'),
('BTG Granada', 'Cali'),
('BTG Centro', 'Barranquilla');

INSERT INTO inscripcion (idCliente, idProducto, fechaInscripcion, estado) VALUES
(1, 1, '2024-01-15', 'ACTIVA'),
(1, 2, '2024-02-20', 'ACTIVA'),
(2, 2, '2024-01-10', 'ACTIVA'),
(2, 3, '2024-03-05', 'ACTIVA'),
(3, 1, '2024-02-01', 'ACTIVA'),
(4, 2, '2024-01-25', 'ACTIVA'),
(5, 3, '2024-02-05', 'ACTIVA'),
(5, 4, '2024-02-10', 'ACTIVA');

INSERT INTO disponibilidad (idSucursal, idProducto, cantidad, precio) VALUES
(1, 1, 100, 100000.00),
(1, 2, 50, 150000.00),
(2, 1, 80, 100000.00),
(2, 4, 60, 250000.00),
(3, 2, 65, 150000.00),
(3, 3, 85, 200000.00),
(5, 3, 70, 200000.00),
(5, 4, 45, 300000.00);

INSERT INTO visitan (idCliente, idSucursal, fechaVisita, motivo) VALUES
(1, 1, '2024-01-10', 'Consulta de productos'),
(1, 2, '2024-02-15', 'Renovación de contrato'),
(2, 3, '2024-01-05', 'Apertura de cuenta'),
(3, 4, '2024-01-20', 'Inscripción a fondo'),
(4, 1, '2024-01-15', 'Consulta de productos'),
(5, 5, '2024-01-25', 'Apertura de cuenta');
