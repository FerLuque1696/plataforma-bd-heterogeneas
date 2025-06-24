import pytest
from sqlalchemy import create_engine, inspect, text

@pytest.fixture
def engine_sqlite():
    # Motor de prueba en memoria con dos tablas y una FK
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE clientes (
                id_cliente INTEGER PRIMARY KEY,
                nombre TEXT
            )
        """))
        conn.execute(text("""
            CREATE TABLE ventas (
                id_venta INTEGER PRIMARY KEY,
                id_cliente INTEGER,
                total REAL,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
            )
        """))
    return engine

def test_columnas_existentes(engine_sqlite):
    inspector = inspect(engine_sqlite)
    columnas = inspector.get_columns("ventas")
    nombres_col = [col["name"] for col in columnas]

    assert "id_venta" in nombres_col
    assert "id_cliente" in nombres_col
    assert "total" in nombres_col

def test_relaciones_detectadas(engine_sqlite):
    inspector = inspect(engine_sqlite)
    fks = inspector.get_foreign_keys("ventas")

    assert len(fks) == 1, "Debe haber una relación definida"
    fk = fks[0]
    assert fk["referred_table"] == "clientes"
    assert fk["constrained_columns"] == ["id_cliente"]
    assert fk["referred_columns"] == ["id_cliente"]
