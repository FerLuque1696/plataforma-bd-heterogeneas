# Importamos clases para definir columnas y tipos de datos
from sqlalchemy import Column, Integer, String

# Importamos la clase base para crear modelos ORM
from sqlalchemy.orm import declarative_base

# Declaramos la clase base a partir de la cual se definirán las tablas
Base = declarative_base()

# Definimos un modelo llamado 'Usuario' que representa la tabla 'usuarios'
class Usuario(Base):
    """Modelo de tabla 'usuarios' compatible con SQLAlchemy ORM."""

    # Nombre real de la tabla en la base de datos
    __tablename__ = "usuarios"

    # Columnas de la tabla y sus tipos
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID único, autoincremental
    nombre = Column(String(100))  # Campo de texto para el nombre (máx. 100 caracteres)
    email = Column(String(100))   # Campo de texto para el email (máx. 100 caracteres)

    # Representación en texto del objeto cuando se imprime
    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"
