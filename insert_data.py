from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import DATABASES
from models import Base, Usuario

def insertar_usuarios(db_key):
    """Inserta usuarios de prueba en la base de datos especificada."""
    print(f"📥 Insertando en: {db_key}")
    
    engine = create_engine(DATABASES[db_key])
    
    # Crear las tablas si no existen
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Usuarios de ejemplo
        usuarios = [
            Usuario(nombre="Fernando Luque", email="fernando@upao.edu.pe"),
            Usuario(nombre="Walter Cueva", email="wcueva@upao.edu.pe"),
            Usuario(nombre="Vladimir Urrello", email="vurello@upao.edu.pe"),
        ]

        session.add_all(usuarios)
        session.commit()
        print("✅ Datos insertados con éxito.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error al insertar datos: {e}")
    finally:
        session.close()

# Ejecutar inserción en todas las bases de datos si se ejecuta directamente
if __name__ == "__main__":
    insertar_usuarios("sqlite")
    insertar_usuarios("postgres")
    insertar_usuarios("mysql")
