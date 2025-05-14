DROP TABLE IF EXISTS detalle_venta;
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100),
    ciudad VARCHAR(50)
);


CREATE TABLE productos (
    id_producto INT PRIMARY KEY,
    nombre VARCHAR(100),
    categoria VARCHAR(50),
    precio DECIMAL(10,2)
);


CREATE TABLE ventas (
    id_venta INT PRIMARY KEY,
    fecha DATE,
    id_cliente INT,
    total DECIMAL(10,2),
    FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente)
);


CREATE TABLE detalle_venta (
    id_detalle INT PRIMARY KEY,
    id_venta INT,
    id_producto INT,
    cantidad INT,
    subtotal DECIMAL(10,2),
    FOREIGN KEY(id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY(id_producto) REFERENCES productos(id_producto)
);

INSERT INTO clientes VALUES (1, 'Cliente_1', 'cliente1@correo.com', 'Barranquilla');
INSERT INTO clientes VALUES (2, 'Cliente_2', 'cliente2@correo.com', 'Medellín');
INSERT INTO clientes VALUES (3, 'Cliente_3', 'cliente3@correo.com', 'Cartagena');
INSERT INTO clientes VALUES (4, 'Cliente_4', 'cliente4@correo.com', 'Bogotá');
INSERT INTO clientes VALUES (5, 'Cliente_5', 'cliente5@correo.com', 'Cartagena');
INSERT INTO clientes VALUES (6, 'Cliente_6', 'cliente6@correo.com', 'Cartagena');
INSERT INTO clientes VALUES (7, 'Cliente_7', 'cliente7@correo.com', 'Bogotá');
INSERT INTO clientes VALUES (8, 'Cliente_8', 'cliente8@correo.com', 'Cali');
INSERT INTO clientes VALUES (9, 'Cliente_9', 'cliente9@correo.com', 'Cartagena');
INSERT INTO clientes VALUES (10, 'Cliente_10', 'cliente10@correo.com', 'Medellín');
INSERT INTO productos VALUES (1, 'Producto_1', 'Libros', 137.56);
INSERT INTO productos VALUES (2, 'Producto_2', 'Deportes', 128.99);
INSERT INTO productos VALUES (3, 'Producto_3', 'Belleza', 105.75);
INSERT INTO productos VALUES (4, 'Producto_4', 'Belleza', 144.75);
INSERT INTO productos VALUES (5, 'Producto_5', 'Belleza', 54.08);
INSERT INTO productos VALUES (6, 'Producto_6', 'Hogar', 71.47);
INSERT INTO productos VALUES (7, 'Producto_7', 'Belleza', 54.1);
INSERT INTO productos VALUES (8, 'Producto_8', 'Libros', 94.41);
INSERT INTO productos VALUES (9, 'Producto_9', 'Hogar', 98.6);
INSERT INTO productos VALUES (10, 'Producto_10', 'Hogar', 140.48);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (1, '2024-05-20', 1, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (2, '2024-05-22', 2, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (3, '2024-05-17', 7, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (4, '2024-05-26', 6, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (5, '2024-05-08', 3, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (6, '2024-05-18', 7, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (7, '2024-05-06', 4, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (8, '2024-05-20', 5, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (9, '2024-05-18', 4, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (10, '2024-05-23', 6, 0.00);
INSERT INTO detalle_venta VALUES (1, 1, 8, 2, 281.66);
INSERT INTO detalle_venta VALUES (2, 1, 7, 2, 256.92);
INSERT INTO detalle_venta VALUES (3, 2, 4, 4, 94.48);
INSERT INTO detalle_venta VALUES (4, 2, 8, 1, 76.89);
INSERT INTO detalle_venta VALUES (5, 3, 9, 2, 141.08);
INSERT INTO detalle_venta VALUES (6, 3, 5, 1, 99.09);
INSERT INTO detalle_venta VALUES (7, 4, 5, 2, 64.42);
INSERT INTO detalle_venta VALUES (8, 4, 4, 2, 286.86);
INSERT INTO detalle_venta VALUES (9, 5, 4, 5, 355.05);
INSERT INTO detalle_venta VALUES (10, 5, 6, 2, 223.32);
INSERT INTO detalle_venta VALUES (11, 6, 6, 1, 102.3);
INSERT INTO detalle_venta VALUES (12, 6, 5, 5, 615.25);
INSERT INTO detalle_venta VALUES (13, 7, 2, 1, 115.99);
INSERT INTO detalle_venta VALUES (14, 7, 8, 2, 282.78);
INSERT INTO detalle_venta VALUES (15, 8, 9, 1, 93.33);
INSERT INTO detalle_venta VALUES (16, 8, 1, 4, 286.0);
INSERT INTO detalle_venta VALUES (17, 9, 7, 4, 374.0);
INSERT INTO detalle_venta VALUES (18, 9, 5, 2, 200.94);
INSERT INTO detalle_venta VALUES (19, 10, 2, 1, 33.78);
INSERT INTO detalle_venta VALUES (20, 10, 7, 4, 523.08);
UPDATE ventas SET total = 538.58 WHERE id_venta = 1;
UPDATE ventas SET total = 171.37 WHERE id_venta = 2;
UPDATE ventas SET total = 240.17 WHERE id_venta = 3;
UPDATE ventas SET total = 351.28 WHERE id_venta = 4;
UPDATE ventas SET total = 578.37 WHERE id_venta = 5;
UPDATE ventas SET total = 717.55 WHERE id_venta = 6;
UPDATE ventas SET total = 398.77 WHERE id_venta = 7;
UPDATE ventas SET total = 379.33 WHERE id_venta = 8;
UPDATE ventas SET total = 574.94 WHERE id_venta = 9;
UPDATE ventas SET total = 556.86 WHERE id_venta = 10;