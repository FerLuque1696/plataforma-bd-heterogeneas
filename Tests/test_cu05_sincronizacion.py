import sys, os
sys.path.append(os.path.abspath("."))

import pytest
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String
from sync_logic import sync_universal

@pytest.fixture
def motores_sync():
    engine1 = create_engine("sqlite:///:memory:")
    engine2 = create_engine("sqlite:///:memory:")

    metadata = MetaData()
    clientes = Table("clientes", metadata,
        Column("id_cliente", Integer, primary_key=True, autoincrement=True),
        Column("nombre", String, nullable=False),
        Column("correo", String, nullable=False, unique=True),
        Column("ciudad", String, nullable=False)
    )

    metadata.create_all(engine1)
    metadata.create_all(engine2)

    return engine1, engine2

def test_insert_sincronizado(motores_sync):
    engine1, engine2 = motores_sync
    nuevo = {"nombre": "Juan", "correo": "juan@correo.com", "ciudad": "Tacna"}

    sync_universal(
        action="insert",
        table_name="clientes",
        record_dict=nuevo,
        db_origen=engine1,
        db_destinos=[engine2],
        unique_keys=["correo"]
    )

    df_destino = pd.read_sql("SELECT * FROM clientes", engine2)
    assert df_destino.shape[0] == 1
    assert "juan@correo.com" in df_destino["correo"].values

def test_update_sincronizado(motores_sync):
    engine1, engine2 = motores_sync
    original = {"nombre": "Carlos", "correo": "carlos@correo.com", "ciudad": "Piura"}
    actualizado = {"nombre": "Carlos A.", "correo": "carlos@correo.com", "ciudad": "Chiclayo"}

    for engine in [engine1, engine2]:
        pd.DataFrame([original]).to_sql("clientes", engine, if_exists="append", index=False)

    sync_universal(
        action="update",
        table_name="clientes",
        record_dict=actualizado,
        db_origen=engine1,
        db_destinos=[engine2],
        unique_keys=["correo"]
    )

    df = pd.read_sql("SELECT * FROM clientes WHERE correo='carlos@correo.com'", engine2)
    assert df.iloc[0]["ciudad"] == "Chiclayo"

def test_delete_sincronizado(motores_sync):
    engine1, engine2 = motores_sync
    registro = {"nombre": "Luis", "correo": "luis@correo.com", "ciudad": "Cusco"}

    for engine in [engine1, engine2]:
        pd.DataFrame([registro]).to_sql("clientes", engine, if_exists="append", index=False)

    sync_universal(
        action="delete",
        table_name="clientes",
        record_dict=registro,
        db_origen=engine1,
        db_destinos=[engine2],
        unique_keys=["correo"]
    )

    df = pd.read_sql("SELECT * FROM clientes WHERE correo='luis@correo.com'", engine2)
    assert df.empty, "El registro debe ser eliminado del motor destino"
