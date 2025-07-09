# PU_limpiar_dataframe.py

import pytest
import pandas as pd
from utils.sync_logic import limpiar_dataframe

def test_limpiar_dataframe_con_objetos():
    df_original = pd.DataFrame({
        "id": [1, 2],
        "fecha": [pd.Timestamp("2024-01-01"), pd.Timestamp("2024-01-02")],
        "custom": [object(), object()]  # Tipos no estándar
    })

    df_limpio = limpiar_dataframe(df_original)

    # Verificamos que no haya tipos object que no sean válidos
    for col in df_limpio.columns:
        assert all(isinstance(val, (int, float, str, bool, type(None), pd.Timestamp)) for val in df_limpio[col])
