import pytest
import pandas as pd
from sqlalchemy import create_engine, text

@pytest.fixture
def motores_sqlite():
    # Crear dos motores SQLite en memoria con estructuras equivalentes
    engine_a = create_engine("sqlite:///:memory:")
    engine_b = create_engine("sqlite:///:memory:")

    with engine_a.begin() as conn:
        conn.execute(text("""
            CREATE TABLE clientes (
                id_cliente INTEGER PRIMARY KEY,
                nombre TEXT,
                correo TEXT,
                ciudad TEXT
            );
        """))
        conn.execute(text("""
            INSERT INTO clientes (nombre, correo, ciudad) VALUES
            ('Fernando', 'fernando@correo.com', 'Trujillo'),
            ('Ana', 'ana@correo.com', 'Lima');
        """))

    with engine_b.begin() as conn:
        conn.execute(text("""
            CREATE TABLE clientes (
                id_cliente INTEGER PRIMARY KEY,
                nombre TEXT,
                correo TEXT,
                ciudad TEXT
            );
        """))
        conn.execute(text("""
            INSERT INTO clientes (nombre, correo, ciudad) VALUES
            ('Fernando', 'fernando@correo.com', 'Trujillo'),
            ('Luis', 'luis@correo.com', 'Cusco');
        """))

    return engine_a, engine_b

def test_integracion_sin_duplicados(motores_sqlite):
    engine_a, engine_b = motores_sqlite

    df_a = pd.read_sql("SELECT nombre, correo, ciudad FROM clientes", engine_a)
    df_b = pd.read_sql("SELECT nombre, correo, ciudad FROM clientes", engine_b)

    # Unificar por columnas equivalentes
    df_merged = pd.concat([df_a, df_b], ignore_index=True).drop_duplicates()

    assert df_merged.shape[0] == 3, "Debe haber 3 registros únicos integrados"
    assert "Luis" in df_merged["nombre"].values
    assert "Ana" in df_merged["nombre"].values
