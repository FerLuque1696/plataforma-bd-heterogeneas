from sqlalchemy import Table, MetaData, select, insert, update, delete, and_
from sqlalchemy.exc import SQLAlchemyError

def sync_universal(action, table_name, record_dict, db_origen, db_destinos, unique_keys):
    """
    Sincroniza un registro en todas las BD destino.
    
    action: "insert", "update", "delete"
    table_name: str
    record_dict: dict con los campos y valores
    db_origen: engine origen (no se vuelve a escribir aquí)
    db_destinos: lista de engines SQLAlchemy
    unique_keys: lista de campos clave para identificar duplicados
    """
    for engine in db_destinos:
        if engine == db_origen:
            continue  # evitar duplicar en la BD de origen

        try:
            metadata = MetaData()
            metadata.reflect(bind=engine)
            table = metadata.tables[table_name]

            # construir filtro de comparación (por campos únicos)
            filtro = and_(*[table.c[k] == record_dict[k] for k in unique_keys])

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
