# PU_sync_universal_tabla_inexistente.py

import pytest
import pandas as pd
from sqlalchemy import create_engine
from utils.sync_logic import sync_universal

def test_sync_universal_tabla_inexistente():
    # Motor SQLite vacío (sin ninguna tabla creada)
    engine = create_engine("sqlite:///:memory:")

    motores = {"sqlite_test": engine}
    df = pd.DataFrame({"id": [1], "nombre": ["Luis"]})
    columnas = ["id", "nombre"]

    resultado = sync_universal(df, motores, "clientes", columnas)

    assert "sqlite_test" in resultado
    assert "no existe" in resultado["sqlite_test"].lower()
