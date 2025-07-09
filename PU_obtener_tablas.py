# PU_obtener_tablas.py

import pytest
from sqlalchemy import create_engine, MetaData, Table, Column, Integer
import streamlit as st
from modulos.integracion import obtener_tablas

@pytest.fixture
def setup_motor_sqlite():
    engine = create_engine("sqlite:///:memory:")
    metadata = MetaData()
    Table("clientes", metadata, Column("id", Integer, primary_key=True)).create(engine)
    Table("productos", metadata, Column("id", Integer, primary_key=True)).create(engine)

    # Simula el motor en la sesión de Streamlit
    st.session_state.motores_conectados = {"test_sqlite": engine}
    return "test_sqlite"

def test_obtener_tablas(setup_motor_sqlite):
    motor_key = setup_motor_sqlite
    tablas = obtener_tablas(motor_key)

    assert "clientes" in tablas
    assert "productos" in tablas
    assert len(tablas) == 2
