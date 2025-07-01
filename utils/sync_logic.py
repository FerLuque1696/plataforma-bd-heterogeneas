import pandas as pd
from sqlalchemy import inspect

# Función de limpieza general
def limpiar_dataframe(df):
    return df.applymap(lambda x: str(x) if not isinstance(x, (int, float, str, bool, type(None), pd.Timestamp)) else x)

def sync_universal(df_integrado, motores, tabla_destino, columnas_destino):
    resultados = {}

    for motor, engine in motores.items():
        try:
            insp = inspect(engine)
            if tabla_destino not in insp.get_table_names():
                resultados[motor] = "❌ Tabla destino no existe"
                continue

            # Verificamos columnas reales del destino
            columnas_bd = [col["name"] for col in insp.get_columns(tabla_destino)]

            # Filtramos columnas válidas (solo aquellas que existen en el destino)
            columnas_validas = [col for col in columnas_destino if col in columnas_bd]
            if not columnas_validas:
                resultados[motor] = "❌ No hay columnas compatibles para sincronizar"
                continue

            # Leemos datos actuales en destino
            df_bd = pd.read_sql(f"SELECT {', '.join(columnas_validas)} FROM {tabla_destino}", engine).drop_duplicates()

            # Preparamos nuevo DataFrame con columnas válidas
            df_nueva = df_integrado[columnas_validas].drop_duplicates()

            # Si hay clave para comparar (usamos la primera columna como ID si está presente)
            if not df_bd.empty and columnas_validas[0] in df_bd.columns:
                clave = columnas_validas[0]
                df_merged = pd.merge(df_nueva, df_bd, how="left", on=clave, indicator=True)
                df_final = df_merged[df_merged["_merge"] == "left_only"].drop(columns=["_merge"])
            else:
                df_final = df_nueva

            if df_final.empty:
                resultados[motor] = "🔁 Sin cambios (todo sincronizado)"
            else:
                # Limpieza para evitar errores de serialización con Arrow y SQLAlchemy
                df_final_limpio = limpiar_dataframe(df_final)

                # Inserta nuevos datos
                df_final_limpio.to_sql(tabla_destino, engine, index=False, if_exists="append", method="multi")
                resultados[motor] = f"✅ Insertados: {len(df_final_limpio)} nuevos registros"
        except Exception as e:
            resultados[motor] = f"⚠️ Error: {str(e)}"

    return resultados
