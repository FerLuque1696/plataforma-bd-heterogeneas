-- Script de creación de la base de datos: tienda_sqlite

CREATE DATABASE tienda_sqlite;
GO
USE tienda_sqlite;

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    correo VARCHAR(100) UNIQUE,
    ciudad VARCHAR(50),
    educacion VARCHAR(50),
    genero VARCHAR(10)
);

CREATE TABLE productos (
    id_producto INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(100),
    precio DECIMAL(10,2),
    categoria VARCHAR(50),
    inventario INT
);

CREATE TABLE ventas (
    id_venta INT PRIMARY KEY IDENTITY(1,1),
    id_cliente INT,
    fecha DATE,
    vendedor VARCHAR(50),
    descripcion TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE detalle_venta (
    id_detalle INT PRIMARY KEY IDENTITY(1,1),
    id_venta INT,
    id_producto INT,
    cantidad INT,
    precio_unitario DECIMAL(10,2),
    subtotal DECIMAL(10,2),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

