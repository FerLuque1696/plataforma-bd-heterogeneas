# validators.py

import pandas as pd  # Usamos pandas para trabajar con datos tabulares fácilmente

# Lista de valores válidos que puede tener el campo 'origen'
ORIGENES_VALIDOS = {"sqlite", "postgres", "mysql","sqlserver"}

# ---------------------------------------------
# FUNCIÓN: validar_datos
# ---------------------------------------------

def validar_datos(lista_usuarios):
    """
    Realiza validaciones sobre una lista de usuarios unificados.
    Devuelve una lista de advertencias si hay errores encontrados.
    Si no hay problemas, la lista de advertencias será vacía.
    """
    advertencias = []

    # Si la lista está vacía, devolvemos una advertencia directa
    if not lista_usuarios:
        return ["❌ La lista de usuarios está vacía."]

    # Convertimos la lista de usuarios (diccionarios) a un DataFrame de pandas
    df = pd.DataFrame(lista_usuarios)

    # -----------------------------------
    # Validación 1: Campos nulos
    # Verifica si hay usuarios sin nombre o sin email
    # -----------------------------------
    nulos = df[df[['nombre', 'email']].isnull().any(axis=1)]
    if not nulos.empty:
        advertencias.append(f"⚠️ {len(nulos)} registro(s) con campos nulos en 'nombre' o 'email'.")

    # -----------------------------------
    # Validación 2: IDs duplicados
    # Verifica si existen usuarios repetidos por 'id' + 'origen'
    # -----------------------------------
    duplicados = df[df.duplicated(subset=['id', 'origen'], keep=False)]
    if not duplicados.empty:
        advertencias.append(f"⚠️ {len(duplicados)} registro(s) con ID duplicado por 'id' y 'origen'.")

    # -----------------------------------
    # Validación 3: Origen inválido
    # Asegura que el campo 'origen' solo tenga valores permitidos
    # -----------------------------------
    origenes_invalidos = df[~df['origen'].isin(ORIGENES_VALIDOS)]
    if not origenes_invalidos.empty:
        advertencias.append(f"⚠️ {len(origenes_invalidos)} registro(s) con origen inválido.")

    # Retornamos todas las advertencias encontradas
    return advertencias

