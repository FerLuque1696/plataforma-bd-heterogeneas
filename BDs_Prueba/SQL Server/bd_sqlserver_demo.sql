USE bd_sqlserver_demo;
GO

IF OBJECT_ID('detalle_venta', 'U') IS NOT NULL DROP TABLE detalle_venta;
IF OBJECT_ID('ventas', 'U') IS NOT NULL DROP TABLE ventas;
IF OBJECT_ID('productos', 'U') IS NOT NULL DROP TABLE productos;
IF OBJECT_ID('clientes', 'U') IS NOT NULL DROP TABLE clientes;


CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nombre NVARCHAR(100),
    correo NVARCHAR(100),
    ciudad NVARCHAR(50)
);


CREATE TABLE productos (
    id_producto INT PRIMARY KEY,
    nombre NVARCHAR(100),
    categoria NVARCHAR(50),
    precio DECIMAL(10,2)
);


CREATE TABLE ventas (
    id_venta INT PRIMARY KEY,
    fecha DATE,
    id_cliente INT FOREIGN KEY REFERENCES clientes(id_cliente),
    total DECIMAL(10,2)
);


CREATE TABLE detalle_venta (
    id_detalle INT PRIMARY KEY,
    id_venta INT FOREIGN KEY REFERENCES ventas(id_venta),
    id_producto INT FOREIGN KEY REFERENCES productos(id_producto),
    cantidad INT,
    subtotal DECIMAL(10,2)
);

INSERT INTO clientes VALUES (1, 'Cliente_1', 'cliente1@ejemplo.com', 'Valparaíso');
INSERT INTO clientes VALUES (2, 'Cliente_2', 'cliente2@ejemplo.com', 'Temuco');
INSERT INTO clientes VALUES (3, 'Cliente_3', 'cliente3@ejemplo.com', 'Temuco');
INSERT INTO clientes VALUES (4, 'Cliente_4', 'cliente4@ejemplo.com', 'Valparaíso');
INSERT INTO clientes VALUES (5, 'Cliente_5', 'cliente5@ejemplo.com', 'Rancagua');
INSERT INTO clientes VALUES (6, 'Cliente_6', 'cliente6@ejemplo.com', 'Valparaíso');
INSERT INTO clientes VALUES (7, 'Cliente_7', 'cliente7@ejemplo.com', 'Santiago');
INSERT INTO clientes VALUES (8, 'Cliente_8', 'cliente8@ejemplo.com', 'Iquique');
INSERT INTO clientes VALUES (9, 'Cliente_9', 'cliente9@ejemplo.com', 'Iquique');
INSERT INTO clientes VALUES (10, 'Cliente_10', 'cliente10@ejemplo.com', 'Iquique');
INSERT INTO productos VALUES (1, 'Producto_1', 'Electrodomésticos', 99.51);
INSERT INTO productos VALUES (2, 'Producto_2', 'Salud', 103.92);
INSERT INTO productos VALUES (3, 'Producto_3', 'Calzado', 131.54);
INSERT INTO productos VALUES (4, 'Producto_4', 'Salud', 152.65);
INSERT INTO productos VALUES (5, 'Producto_5', 'Papelería', 37.33);
INSERT INTO productos VALUES (6, 'Producto_6', 'Electrodomésticos', 28.71);
INSERT INTO productos VALUES (7, 'Producto_7', 'Salud', 177.28);
INSERT INTO productos VALUES (8, 'Producto_8', 'Salud', 59.32);
INSERT INTO productos VALUES (9, 'Producto_9', 'Calzado', 100.04);
INSERT INTO productos VALUES (10, 'Producto_10', 'Electrodomésticos', 150.23);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (1, '2024-05-01', 1, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (2, '2024-05-20', 1, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (3, '2024-05-13', 5, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (4, '2024-05-12', 2, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (5, '2024-05-24', 9, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (6, '2024-05-08', 7, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (7, '2024-05-15', 1, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (8, '2024-05-19', 8, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (9, '2024-05-19', 7, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (10, '2024-05-03', 1, 0.00);
INSERT INTO detalle_venta VALUES (1, 1, 4, 4, 551.28);
INSERT INTO detalle_venta VALUES (2, 1, 2, 1, 155.86);
INSERT INTO detalle_venta VALUES (3, 2, 10, 4, 372.36);
INSERT INTO detalle_venta VALUES (4, 2, 2, 1, 43.66);
INSERT INTO detalle_venta VALUES (5, 3, 5, 2, 94.32);
INSERT INTO detalle_venta VALUES (6, 3, 7, 3, 332.49);
INSERT INTO detalle_venta VALUES (7, 4, 2, 5, 545.95);
INSERT INTO detalle_venta VALUES (8, 4, 10, 1, 41.22);
INSERT INTO detalle_venta VALUES (9, 5, 5, 5, 701.8);
INSERT INTO detalle_venta VALUES (10, 5, 3, 3, 351.3);
INSERT INTO detalle_venta VALUES (11, 6, 4, 3, 369.93);
INSERT INTO detalle_venta VALUES (12, 6, 5, 1, 33.31);
INSERT INTO detalle_venta VALUES (13, 7, 9, 1, 72.32);
INSERT INTO detalle_venta VALUES (14, 7, 3, 4, 232.4);
INSERT INTO detalle_venta VALUES (15, 8, 8, 3, 477.0);
INSERT INTO detalle_venta VALUES (16, 8, 3, 5, 885.5);
INSERT INTO detalle_venta VALUES (17, 9, 7, 5, 486.85);
INSERT INTO detalle_venta VALUES (18, 9, 7, 2, 288.34);
INSERT INTO detalle_venta VALUES (19, 10, 2, 5, 535.85);
INSERT INTO detalle_venta VALUES (20, 10, 5, 4, 226.88);
UPDATE ventas SET total = 707.14 WHERE id_venta = 1;
UPDATE ventas SET total = 416.02 WHERE id_venta = 2;
UPDATE ventas SET total = 426.81 WHERE id_venta = 3;
UPDATE ventas SET total = 587.17 WHERE id_venta = 4;
UPDATE ventas SET total = 1053.1 WHERE id_venta = 5;
UPDATE ventas SET total = 403.24 WHERE id_venta = 6;
UPDATE ventas SET total = 304.72 WHERE id_venta = 7;
UPDATE ventas SET total = 1362.5 WHERE id_venta = 8;
UPDATE ventas SET total = 775.19 WHERE id_venta = 9;
UPDATE ventas SET total = 762.73 WHERE id_venta = 10;