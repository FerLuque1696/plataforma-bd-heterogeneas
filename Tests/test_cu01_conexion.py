import pytest
from sqlalchemy import create_engine, inspect, text

@pytest.fixture
def engine_sqlite():
    # Motor de prueba usando SQLite en memoria
    return create_engine("sqlite:///:memory:")

def test_conexion_exitosa(engine_sqlite):
    try:
        # Intentar conectar
        conn = engine_sqlite.connect()
        conn.close()
        assert True, "Conexión establecida exitosamente"
    except Exception as e:
        pytest.fail(f"Falló la conexión: {e}")

def test_listado_tablas_vacio(engine_sqlite):
    # Confirmar que inicialmente no hay tablas
    inspector = inspect(engine_sqlite)
    tablas = inspector.get_table_names()
    assert isinstance(tablas, list), "Debe retornar una lista"
    assert len(tablas) == 0, "Al inicio no debe haber tablas"

def test_crear_y_listar_tabla(engine_sqlite):
    # Crear tabla temporal y verificar que se liste
    with engine_sqlite.connect() as conn:
        conn.execute(text("CREATE TABLE clientes (id INTEGER PRIMARY KEY, nombre TEXT)"))
        conn.commit()

    inspector = inspect(engine_sqlite)
    tablas = inspector.get_table_names()
    assert "clientes" in tablas, "La tabla 'clientes' debe existir luego de crearla"

