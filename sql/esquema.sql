-- 1. TABLA DE PROVEEDORES
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- 2. TABLA DE CLIENTES
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- 3. TABLA DE PRODUCTOS
CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(100),
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    imagen VARCHAR(255),
    id_proveedor INT,
    CONSTRAINT fk_producto_proveedor FOREIGN KEY (id_proveedor) 
        REFERENCES proveedores(id_proveedor) 
        ON DELETE SET NULL
);

-- 4. TABLA DE FACTURAS
CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    total DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_factura_cliente FOREIGN KEY (id_cliente) 
        REFERENCES clientes(id_cliente) 
        ON DELETE CASCADE
);

-- 5. TABLA DE USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);