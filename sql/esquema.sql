-- ===================================================================
-- ESQUEMA ACTUALIZADO - Boutique Alison (PostgreSQL)
-- ===================================================================

-- 1. PROVEEDORES
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- 2. CLIENTES
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- 3. PRODUCTOS (stock total + stock por talla S, M, L)
CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    stock_s INT DEFAULT 0,
    stock_m INT DEFAULT 0,
    stock_l INT DEFAULT 0,
    imagen VARCHAR(255) NOT NULL,
    id_proveedor INT,
    CONSTRAINT fk_producto_proveedor FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
        ON DELETE SET NULL
);

-- 4. FACTURAS (una fila por producto comprado, como lo guarda app.py)
CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    id_cliente INT,
    cliente VARCHAR(100),
    id_producto INT,
    cantidad INT,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    total DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_factura_cliente FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE CASCADE,
    CONSTRAINT fk_factura_producto FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)
        ON DELETE SET NULL
);

-- 5. USUARIOS (la columna 'rol' distingue administrador y cliente)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'cliente'
);

-- ===================================================================
-- ACTUALIZACIONES PARA UNA BASE YA EXISTENTE
-- (si la columna ya existe, no hace nada)
-- ===================================================================

ALTER TABLE productos ADD COLUMN IF NOT EXISTS stock_s INT DEFAULT 0;
ALTER TABLE productos ADD COLUMN IF NOT EXISTS stock_m INT DEFAULT 0;
ALTER TABLE productos ADD COLUMN IF NOT EXISTS stock_l INT DEFAULT 0;

ALTER TABLE facturas ADD COLUMN IF NOT EXISTS cliente VARCHAR(100);
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS id_producto INT
    REFERENCES productos(id_producto) ON DELETE SET NULL;
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS cantidad INT;

-- ===================================================================
-- DATOS INICIALES
-- ===================================================================

-- Proveedor por defecto (solo si no hay ninguno)
INSERT INTO proveedores (nombre, telefono, correo)
SELECT 'Proveedor General', '0991234567', 'contacto@proveedor.com'
WHERE NOT EXISTS (SELECT 1 FROM proveedores);

-- El usuario administrador NO se inserta aqui.
-- Se crea con el script crear_admin.py, que genera el hash de la
-- contrasena de forma correcta con Werkzeug.