CREATE DATABASE btg;

CREATE SCHEMA IF NOT EXISTS btg_schema;
SET search_path TO btg_schema;
CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE producto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    tipoProducto VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sucursal (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inscripcion (
    idProducto INTEGER NOT NULL,
    idCliente INTEGER NOT NULL,
    fechaInscripcion DATE DEFAULT CURRENT_DATE,
    estado VARCHAR(20) DEFAULT 'ACTIVA',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idProducto, idCliente),
    FOREIGN KEY (idProducto) REFERENCES producto(id) ON DELETE CASCADE,
    FOREIGN KEY (idCliente) REFERENCES cliente(id) ON DELETE CASCADE
);

CREATE TABLE disponibilidad (
    idSucursal INTEGER NOT NULL,
    idProducto INTEGER NOT NULL,
    cantidad INTEGER DEFAULT 0,
    precio DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idSucursal, idProducto),
    FOREIGN KEY (idSucursal) REFERENCES sucursal(id) ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES producto(id) ON DELETE CASCADE
);

CREATE TABLE visitan (
    idSucursal INTEGER NOT NULL,
    idCliente INTEGER NOT NULL,
    fechaVisita DATE NOT NULL,
    motivo VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idSucursal, idCliente, fechaVisita),
    FOREIGN KEY (idSucursal) REFERENCES sucursal(id) ON DELETE CASCADE,
    FOREIGN KEY (idCliente) REFERENCES cliente(id) ON DELETE CASCADE
);

CREATE INDEX idx_cliente_ciudad ON cliente(ciudad);
CREATE INDEX idx_producto_tipo ON producto(tipoProducto);
CREATE INDEX idx_sucursal_ciudad ON sucursal(ciudad);
CREATE INDEX idx_inscripcion_cliente ON inscripcion(idCliente);
CREATE INDEX idx_inscripcion_producto ON inscripcion(idProducto);
CREATE INDEX idx_disponibilidad_sucursal ON disponibilidad(idSucursal);
CREATE INDEX idx_disponibilidad_producto ON disponibilidad(idProducto);
CREATE INDEX idx_visitan_cliente ON visitan(idCliente);
CREATE INDEX idx_visitan_sucursal ON visitan(idSucursal);
CREATE INDEX idx_visitan_fecha ON visitan(fechaVisita);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cliente_updated_at BEFORE UPDATE ON cliente
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_producto_updated_at BEFORE UPDATE ON producto
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sucursal_updated_at BEFORE UPDATE ON sucursal
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_inscripcion_updated_at BEFORE UPDATE ON inscripcion
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_disponibilidad_updated_at BEFORE UPDATE ON disponibilidad
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE schemaname = 'btg_schema'
ORDER BY tablename;
