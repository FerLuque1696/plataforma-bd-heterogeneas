from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Usuario
from config import construir_url
import csv

# -----------------------------------------
# FUNCIÓN: obtener_usuarios
# -----------------------------------------
def obtener_usuarios(db_key):
    """
    Obtiene usuarios desde la base de datos especificada usando su clave.
    Devuelve una lista de diccionarios con los datos obtenidos.
    """
    print(f"🔍 Consultando usuarios en: {db_key}")
    engine = create_engine(construir_url(db_key))
    Session = sessionmaker(bind=engine)
    session = Session()

    usuarios_lista = []

    try:
        usuarios = session.query(Usuario).all()
        for u in usuarios:
            usuarios_lista.append({
                "id": u.id,
                "nombre": u.nombre,
                "email": u.email,
                "origen": db_key
            })
        print(f"✅ {len(usuarios)} usuarios obtenidos desde {db_key}")
    except Exception as e:
        print(f"❌ Error al consultar usuarios en {db_key}: {e}")
    finally:
        session.close()

    return usuarios_lista

# -----------------------------------------
# FUNCIÓN: exportar_csv_unificado
# -----------------------------------------
def exportar_csv_unificado(usuarios_unificados, origen="unificados"):
    """
    Exporta una lista de usuarios (diccionarios) a un archivo CSV.
    El archivo se nombra como 'usuarios_{origen}.csv'
    """
    if not usuarios_unificados:
        raise ValueError("No hay datos unificados para exportar.")

    filename = f"usuarios_{origen}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=usuarios_unificados[0].keys())
        writer.writeheader()
        writer.writerows(usuarios_unificados)

    print(f"✅ Exportación a '{filename}' completada.")
