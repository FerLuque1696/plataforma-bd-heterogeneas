
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE detalle_venta';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE ventas';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE productos';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE clientes';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/


CREATE TABLE clientes (
    id_cliente NUMBER PRIMARY KEY,
    nombre VARCHAR2(100),
    correo VARCHAR2(100),
    ciudad VARCHAR2(50)
);


CREATE TABLE productos (
    id_producto NUMBER PRIMARY KEY,
    nombre VARCHAR2(100),
    categoria VARCHAR2(50),
    precio NUMBER(10,2)
);


CREATE TABLE ventas (
    id_venta NUMBER PRIMARY KEY,
    fecha DATE,
    id_cliente NUMBER,
    total NUMBER(10,2),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);


CREATE TABLE detalle_venta (
    id_detalle NUMBER PRIMARY KEY,
    id_venta NUMBER,
    id_producto NUMBER,
    cantidad NUMBER,
    subtotal NUMBER(10,2),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

INSERT INTO clientes VALUES (1, 'Cliente_1', 'cliente1@demo.com', 'CDMX');
INSERT INTO clientes VALUES (2, 'Cliente_2', 'cliente2@demo.com', 'Guadalajara');
INSERT INTO clientes VALUES (3, 'Cliente_3', 'cliente3@demo.com', 'Puebla');
INSERT INTO clientes VALUES (4, 'Cliente_4', 'cliente4@demo.com', 'CDMX');
INSERT INTO clientes VALUES (5, 'Cliente_5', 'cliente5@demo.com', 'Guadalajara');
INSERT INTO clientes VALUES (6, 'Cliente_6', 'cliente6@demo.com', 'Puebla');
INSERT INTO clientes VALUES (7, 'Cliente_7', 'cliente7@demo.com', 'Guadalajara');
INSERT INTO clientes VALUES (8, 'Cliente_8', 'cliente8@demo.com', 'Guadalajara');
INSERT INTO clientes VALUES (9, 'Cliente_9', 'cliente9@demo.com', 'Monterrey');
INSERT INTO clientes VALUES (10, 'Cliente_10', 'cliente10@demo.com', 'CDMX');
INSERT INTO productos VALUES (1, 'Producto_1', 'Moda', 154.86);
INSERT INTO productos VALUES (2, 'Producto_2', 'Salud', 43.39);
INSERT INTO productos VALUES (3, 'Producto_3', 'Salud', 33.33);
INSERT INTO productos VALUES (4, 'Producto_4', 'Alimentos', 79.96);
INSERT INTO productos VALUES (5, 'Producto_5', 'Alimentos', 189.88);
INSERT INTO productos VALUES (6, 'Producto_6', 'Salud', 27.42);
INSERT INTO productos VALUES (7, 'Producto_7', 'Videojuegos', 166.95);
INSERT INTO productos VALUES (8, 'Producto_8', 'Salud', 46.62);
INSERT INTO productos VALUES (9, 'Producto_9', 'Videojuegos', 117.57);
INSERT INTO productos VALUES (10, 'Producto_10', 'Videojuegos', 27.55);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (1, TO_DATE('2024-05-19', 'YYYY-MM-DD'), 1, 0);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (2, TO_DATE('2024-05-26', 'YYYY-MM-DD'), 2, 0);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (3, TO_DATE('2024-05-08', 'YYYY-MM-DD'), 2, 0);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (4, TO_DATE('2024-05-05', 'YYYY-MM-DD'), 7, 0);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (5, TO_DATE('2024-05-23', 'YYYY-MM-DD'), 6, 0);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (6, TO_DATE('2024-05-19', 'YYYY-MM-DD'), 7, 0);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (7, TO_DATE('2024-05-21', 'YYYY-MM-DD'), 2, 0);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (8, TO_DATE('2024-05-20', 'YYYY-MM-DD'), 8, 0);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (9, TO_DATE('2024-05-22', 'YYYY-MM-DD'), 2, 0);
INSERT INTO ventas(id_venta, fecha, id_cliente, total) VALUES (10, TO_DATE('2024-05-13', 'YYYY-MM-DD'), 3, 0);
INSERT INTO detalle_venta VALUES (1, 1, 7, 1, 142.17);
INSERT INTO detalle_venta VALUES (2, 1, 8, 2, 203.02);
INSERT INTO detalle_venta VALUES (3, 2, 2, 1, 172.13);
INSERT INTO detalle_venta VALUES (4, 2, 9, 4, 297.2);
INSERT INTO detalle_venta VALUES (5, 3, 3, 5, 74.45);
INSERT INTO detalle_venta VALUES (6, 3, 2, 1, 43.4);
INSERT INTO detalle_venta VALUES (7, 4, 2, 1, 26.82);
INSERT INTO detalle_venta VALUES (8, 4, 6, 4, 773.56);
INSERT INTO detalle_venta VALUES (9, 5, 1, 2, 282.8);
INSERT INTO detalle_venta VALUES (10, 5, 1, 5, 875.5);
INSERT INTO detalle_venta VALUES (11, 6, 4, 5, 406.1);
INSERT INTO detalle_venta VALUES (12, 6, 2, 3, 348.33);
INSERT INTO detalle_venta VALUES (13, 7, 10, 4, 678.24);
INSERT INTO detalle_venta VALUES (14, 7, 3, 4, 728.76);
INSERT INTO detalle_venta VALUES (15, 8, 2, 4, 743.64);
INSERT INTO detalle_venta VALUES (16, 8, 2, 5, 414.65);
INSERT INTO detalle_venta VALUES (17, 9, 1, 5, 688.05);
INSERT INTO detalle_venta VALUES (18, 9, 10, 5, 452.95);
INSERT INTO detalle_venta VALUES (19, 10, 2, 1, 73.7);
INSERT INTO detalle_venta VALUES (20, 10, 1, 2, 324.08);
UPDATE ventas SET total = 345.19 WHERE id_venta = 1;
UPDATE ventas SET total = 469.33 WHERE id_venta = 2;
UPDATE ventas SET total = 117.85 WHERE id_venta = 3;
UPDATE ventas SET total = 800.38 WHERE id_venta = 4;
UPDATE ventas SET total = 1158.3 WHERE id_venta = 5;
UPDATE ventas SET total = 754.43 WHERE id_venta = 6;
UPDATE ventas SET total = 1407.0 WHERE id_venta = 7;
UPDATE ventas SET total = 1158.29 WHERE id_venta = 8;
UPDATE ventas SET total = 1141.0 WHERE id_venta = 9;
UPDATE ventas SET total = 397.78 WHERE id_venta = 10;