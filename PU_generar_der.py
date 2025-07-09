# PU_generar_der.py
from modulos.exploracion import generar_der
from sqlalchemy import create_engine, inspect, text
import pytest
import os

def test_generar_diagrama_er(tmp_path):
    # Crear una base de datos SQLite temporal con dos tablas relacionadas
    ruta_db = tmp_path / "test_der.db"
    engine = create_engine(f"sqlite:///{ruta_db}")
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE clientes (
                id INTEGER PRIMARY KEY,
                nombre TEXT
            );
        """))
        conn.execute(text("""
            CREATE TABLE pedidos (
                id INTEGER PRIMARY KEY,
                cliente_id INTEGER,
                producto TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            );
        """))

    # Validación básica: no debe lanzar excepción al generar DER
    try:
        generar_der(engine, "sqlite")
    except Exception as e:
        pytest.fail(f"Error inesperado al generar DER: {e}")
