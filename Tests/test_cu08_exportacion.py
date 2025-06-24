import pytest
import pandas as pd
from io import StringIO

@pytest.fixture
def datos_integrados():
    # DataFrame simulado luego de integración
    return pd.DataFrame([
        {"nombre": "Mario", "correo": "mario@correo.com", "ciudad": "Lima"},
        {"nombre": "Lucia", "correo": "lucia@correo.com", "ciudad": "Arequipa"},
        {"nombre": "Juan", "correo": "juan@correo.com", "ciudad": "Tacna"}
    ])

def test_exportacion_csv(datos_integrados):
    buffer = StringIO()
    datos_integrados.to_csv(buffer, index=False)

    contenido = buffer.getvalue()

    assert "nombre,correo,ciudad" in contenido
    assert "mario@correo.com" in contenido
    assert contenido.count("@correo.com") == 3
    assert len(contenido.splitlines()) == 4  # 1 encabezado + 3 registros
