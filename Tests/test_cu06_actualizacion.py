import sys, os
sys.path.append(os.path.abspath("."))

import pytest
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String
from sync_logic import sync_universal

@pytest.fixture
def motores_update():
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

    original = {"nombre": "Carlos", "correo": "carlos@correo.com", "ciudad": "Piura"}
    for engine in [engine1, engine2]:
        pd.DataFrame([original]).to_sql("clientes", engine, if_exists="append", index=False)

    return engine1, engine2

def test_actualizacion_manual_sincronizada(motores_update):
    engine1, engine2 = motores_update
    actualizado = {"nombre": "Carlos A.", "correo": "carlos@correo.com", "ciudad": "Chiclayo"}

    sync_universal(
        action="update",
        table_name="clientes",
        record_dict=actualizado,
        db_origen=engine1,
        db_destinos=[engine2],
        unique_keys=["correo"]
    )

    df_sync = pd.read_sql("SELECT * FROM clientes WHERE correo='carlos@correo.com'", engine2)
    assert df_sync.iloc[0]["ciudad"] == "Chiclayo"
    assert df_sync.iloc[0]["nombre"] == "Carlos A."
