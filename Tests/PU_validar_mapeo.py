# tests/PU_validar_generico.py

import pytest
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from validators import validar_generico

@pytest.fixture(scope="module")
def engine_sqlite():
    # Creamos motor SQLite en memoria
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE clientes (
                id_cliente INTEGER PRIMARY KEY NOT NULL,
                nombre TEXT NOT NULL,
                correo TEXT
            )
        """))
    return engine

def test_validar_generico_sin_errores(engine_sqlite):
    df = pd.DataFrame({
        "id_cliente": [1, 2],
        "nombre": ["Juan", "Ana"],
        "correo": ["a@a.com", "b@b.com"]
    })
    advertencias = validar_generico(df, engine_sqlite, "clientes")
    assert advertencias == []

def test_validar_generico_con_nulos(engine_sqlite):
    df = pd.DataFrame({
        "id_cliente": [1, None],
        "nombre": ["Juan", None],
        "correo": ["a@a.com", "b@b.com"]
    })
    advertencias = validar_generico(df, engine_sqlite, "clientes")
    assert any("no puede tener valores nulos" in a.lower() for a in advertencias)

def test_validar_generico_con_duplicados(engine_sqlite):
    df = pd.DataFrame({
        "id_cliente": [1, 1],
        "nombre": ["Juan", "Juan"],
        "correo": ["a@a.com", "a@a.com"]
    })
    advertencias = validar_generico(df, engine_sqlite, "clientes")
    assert any("duplicados" in a.lower() for a in advertencias)
