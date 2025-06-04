# validators.py
import pandas as pd
from sqlalchemy import inspect

def validar_generico(df: pd.DataFrame, engine, tabla_destino: str):
    """
    Valida que los datos en el DataFrame sean compatibles con la tabla destino:
    - No deben existir valores nulos en columnas NOT NULL
    - No deben existir claves primarias duplicadas
    """
    advertencias = []
    inspector = inspect(engine)

    # 1. Columnas NOT NULL
    columnas_info = inspector.get_columns(tabla_destino)
    columnas_not_null = [col["name"] for col in columnas_info if not col.get("nullable", True)]

    for col in columnas_not_null:
        if col in df.columns and df[col].isnull().any():
            advertencias.append(f"❌ La columna '{col}' no puede tener valores nulos.")

    # 2. Clave primaria duplicada (si existe)
    pk_info = inspector.get_pk_constraint(tabla_destino)
    claves_primarias = pk_info.get("constrained_columns", [])

    if claves_primarias:
        if all(col in df.columns for col in claves_primarias):
            duplicados = df.duplicated(subset=claves_primarias).sum()
            if duplicados > 0:
                advertencias.append(
                    f"⚠️ Hay {duplicados} registros duplicados en la clave primaria ({', '.join(claves_primarias)})."
                )

    return advertencias
