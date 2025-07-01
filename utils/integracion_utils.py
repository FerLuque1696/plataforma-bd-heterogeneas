# utils/integracion_utils.py

import pandas as pd
from sqlalchemy import inspect

def obtener_columnas_compatibles(engine1, tabla1, engine2, tabla2):
    insp1 = inspect(engine1)
    insp2 = inspect(engine2)

    cols1 = {col["name"]: col for col in insp1.get_columns(tabla1)}
    cols2 = {col["name"]: col for col in insp2.get_columns(tabla2)}

    columnas_compatibles = []
    for nombre1, col1 in cols1.items():
        for nombre2, col2 in cols2.items():
            if nombre1.lower() == nombre2.lower():
                if str(col1["type"]).lower()[:5] == str(col2["type"]).lower()[:5]:
                    columnas_compatibles.append((nombre1, nombre2))
    return columnas_compatibles

def integrar_tablas(engine1, tabla1, engine2, tabla2, columnas_compatibles):
    if not columnas_compatibles:
        return pd.DataFrame()

    columnas1 = [col1 for col1, _ in columnas_compatibles]
    columnas2 = [col2 for _, col2 in columnas_compatibles]

    query1 = f"SELECT {', '.join(columnas1)} FROM {tabla1}"
    query2 = f"SELECT {', '.join(columnas2)} FROM {tabla2}"

    df1 = pd.read_sql(query1, engine1)
    df2 = pd.read_sql(query2, engine2)

    # Renombrar columnas del segundo DataFrame para que coincidan
    df2.columns = columnas1

    # Concatenar sin duplicar
    df_integrado = pd.concat([df1, df2], ignore_index=True).drop_duplicates()
    return df_integrado
