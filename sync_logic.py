from sqlalchemy import Table, MetaData, select, insert, update, delete, and_
from sqlalchemy.exc import SQLAlchemyError

def sync_universal(action, table_name, record_dict, db_origen, db_destinos, unique_keys):
    """
    Sincroniza un registro entre múltiples motores de base de datos.
    
    action: 'insert', 'update', o 'delete'
    table_name: nombre de la tabla (str)
    record_dict: diccionario con los datos
    db_origen: motor origen (SQLAlchemy Engine)
    db_destinos: lista de motores destino
    unique_keys: claves lógicas para identificar registros únicos
    """
    for engine in db_destinos:
        if engine == db_origen:
            continue

        try:
            metadata = MetaData()
            metadata.reflect(bind=engine)
            table = metadata.tables[table_name]

            filtro = and_(*[table.c[k] == record_dict[k] for k in unique_keys if k in record_dict])

            with engine.connect() as conn:
                existing = conn.execute(select(table).where(filtro)).fetchone()

                if action == "insert":
                    if not existing:
                        conn.execute(insert(table).values(**record_dict))
                        conn.commit()

                elif action == "update":
                    if existing:
                        conn.execute(update(table).where(filtro).values(**record_dict))
                        conn.commit()

                elif action == "delete":
                    if existing:
                        conn.execute(delete(table).where(filtro))
                        conn.commit()

        except SQLAlchemyError as e:
            print(f"[ERROR] Sync {action.upper()} on {table_name} in {engine.url}: {e}")
        except KeyError as e:
            print(f"[ERROR] Clave faltante en record_dict para {table_name}: {e}")
