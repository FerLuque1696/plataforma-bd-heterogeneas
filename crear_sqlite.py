# crear_sqlite.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

# Definición de base y modelo
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    correo = Column(String)

# Crear archivo .db y tabla en SQLite
engine = create_engine('sqlite:///BDtestTipoSQLite.db')
Base.metadata.create_all(engine)

print("✅ Base de datos SQLite creada correctamente.")
