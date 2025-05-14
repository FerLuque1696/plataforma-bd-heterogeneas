DROP TABLE IF EXISTS detalle_venta CASCADE;
DROP TABLE IF EXISTS ventas CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT,
    correo TEXT,
    ciudad TEXT
);


CREATE TABLE productos (
    id_producto INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    precio NUMERIC(10,2)
);


CREATE TABLE ventas (
    id_venta INTEGER PRIMARY KEY,
    fecha DATE,
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    total NUMERIC(10,2)
);


CREATE TABLE detalle_venta (
    id_detalle INTEGER PRIMARY KEY,
    id_venta INTEGER REFERENCES ventas(id_venta),
    id_producto INTEGER REFERENCES productos(id_producto),
    cantidad INTEGER,
    subtotal NUMERIC(10,2)
);

INSERT INTO clientes VALUES (1, 'Cliente_1', 'cliente1@mail.com', 'Guayaquil');
INSERT INTO clientes VALUES (2, 'Cliente_2', 'cliente2@mail.com', 'Cuenca');
INSERT INTO clientes VALUES (3, 'Cliente_3', 'cliente3@mail.com', 'Quito');
INSERT INTO clientes VALUES (4, 'Cliente_4', 'cliente4@mail.com', 'Loja');
INSERT INTO clientes VALUES (5, 'Cliente_5', 'cliente5@mail.com', 'Quito');
INSERT INTO clientes VALUES (6, 'Cliente_6', 'cliente6@mail.com', 'Ambato');
INSERT INTO clientes VALUES (7, 'Cliente_7', 'cliente7@mail.com', 'Cuenca');
INSERT INTO clientes VALUES (8, 'Cliente_8', 'cliente8@mail.com', 'Quito');
INSERT INTO clientes VALUES (9, 'Cliente_9', 'cliente9@mail.com', 'Loja');
INSERT INTO clientes VALUES (10, 'Cliente_10', 'cliente10@mail.com', 'Guayaquil');
INSERT INTO productos VALUES (1, 'Producto_1', 'Oficina', 159.28);
INSERT INTO productos VALUES (2, 'Producto_2', 'Salud', 95.11);
INSERT INTO productos VALUES (3, 'Producto_3', 'Tecnología', 84.68);
INSERT INTO productos VALUES (4, 'Producto_4', 'Muebles', 67.68);
INSERT INTO productos VALUES (5, 'Producto_5', 'Limpieza', 92.85);
INSERT INTO productos VALUES (6, 'Producto_6', 'Oficina', 187.47);
INSERT INTO productos VALUES (7, 'Producto_7', 'Tecnología', 174.14);
INSERT INTO productos VALUES (8, 'Producto_8', 'Oficina', 75.83);
INSERT INTO productos VALUES (9, 'Producto_9', 'Salud', 89.51);
INSERT INTO productos VALUES (10, 'Producto_10', 'Muebles', 122.7);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (1, '2024-05-27', 4, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (2, '2024-05-10', 9, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (3, '2024-05-25', 1, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (4, '2024-05-27', 5, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (5, '2024-05-13', 2, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (6, '2024-05-20', 9, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (7, '2024-05-19', 10, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (8, '2024-05-23', 4, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (9, '2024-05-17', 7, 0.00);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (10, '2024-05-19', 2, 0.00);
INSERT INTO detalle_venta VALUES (1, 1, 1, 3, 428.52);
INSERT INTO detalle_venta VALUES (2, 1, 8, 3, 376.29);
INSERT INTO detalle_venta VALUES (3, 2, 7, 2, 238.88);
INSERT INTO detalle_venta VALUES (4, 2, 1, 2, 148.56);
INSERT INTO detalle_venta VALUES (5, 3, 9, 5, 973.2);
INSERT INTO detalle_venta VALUES (6, 3, 9, 5, 579.5);
INSERT INTO detalle_venta VALUES (7, 4, 10, 2, 348.36);
INSERT INTO detalle_venta VALUES (8, 4, 9, 4, 607.6);
INSERT INTO detalle_venta VALUES (9, 5, 6, 2, 185.0);
INSERT INTO detalle_venta VALUES (10, 5, 4, 3, 227.07);
INSERT INTO detalle_venta VALUES (11, 6, 2, 4, 246.2);
INSERT INTO detalle_venta VALUES (12, 6, 7, 2, 207.62);
INSERT INTO detalle_venta VALUES (13, 7, 9, 5, 714.15);
INSERT INTO detalle_venta VALUES (14, 7, 8, 4, 387.24);
INSERT INTO detalle_venta VALUES (15, 8, 3, 4, 550.12);
INSERT INTO detalle_venta VALUES (16, 8, 4, 1, 63.14);
INSERT INTO detalle_venta VALUES (17, 9, 7, 5, 812.55);
INSERT INTO detalle_venta VALUES (18, 9, 7, 3, 575.28);
INSERT INTO detalle_venta VALUES (19, 10, 2, 2, 68.42);
INSERT INTO detalle_venta VALUES (20, 10, 1, 5, 865.35);
UPDATE ventas SET total = 804.81 WHERE id_venta = 1;
UPDATE ventas SET total = 387.44 WHERE id_venta = 2;
UPDATE ventas SET total = 1552.7 WHERE id_venta = 3;
UPDATE ventas SET total = 955.96 WHERE id_venta = 4;
UPDATE ventas SET total = 412.07 WHERE id_venta = 5;
UPDATE ventas SET total = 453.82 WHERE id_venta = 6;
UPDATE ventas SET total = 1101.39 WHERE id_venta = 7;
UPDATE ventas SET total = 613.26 WHERE id_venta = 8;
UPDATE ventas SET total = 1387.83 WHERE id_venta = 9;
UPDATE ventas SET total = 933.77 WHERE id_venta = 10;