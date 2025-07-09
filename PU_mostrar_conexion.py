# PU_mostrar_conexion.py

from sqlalchemy import create_engine, inspect
import os
import pytest

def test_conexion_sqlite_y_tablas():
    ruta_db = "BDs_Prueba/SQLite/tienda_sqlite.db"

    # Validar que el archivo existe antes de continuar
    assert os.path.exists(ruta_db), f"No se encontró la base de datos: {ruta_db}"

    try:
        engine = create_engine(f"sqlite:///{ruta_db}")
        inspector = inspect(engine)
        tablas = inspector.get_table_names()
        
        # Asegura que se obtenga al menos una tabla
        assert isinstance(tablas, list), "No se obtuvo una lista de tablas"
        assert all(isinstance(t, str) for t in tablas), "Las tablas no son strings"
        
    except Exception as e:
        pytest.fail(f"Fallo al conectar o inspeccionar tablas: {str(e)}")
