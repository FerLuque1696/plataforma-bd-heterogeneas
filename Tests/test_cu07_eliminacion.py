import sys, os
sys.path.append(os.path.abspath("."))

import pytest
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String
from sync_logic import sync_universal

@pytest.fixture
def motores_delete():
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

    registro = {"nombre": "Luis", "correo": "luis@correo.com", "ciudad": "Cusco"}
    for engine in [engine1, engine2]:
        pd.DataFrame([registro]).to_sql("clientes", engine, if_exists="append", index=False)

    return engine1, engine2

def test_eliminacion_sincronizada(motores_delete):
    engine1, engine2 = motores_delete
    registro = {"nombre": "Luis", "correo": "luis@correo.com", "ciudad": "Cusco"}

    sync_universal(
        action="delete",
        table_name="clientes",
        record_dict=registro,
        db_origen=engine1,
        db_destinos=[engine2],
        unique_keys=["correo"]
    )

    df_post = pd.read_sql("SELECT * FROM clientes WHERE correo='luis@correo.com'", engine2)
    assert df_post.empty, "El registro debe ser eliminado del motor destino"
