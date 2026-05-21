"""
Configuração central dos testes: banco em memória e fixtures reutilizáveis.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from database import get_session
from main import app

TEST_DATABASE_URL = "sqlite://"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def marca(client: TestClient) -> dict:
    resp = client.post("/marcas/", json={"nome_marca": "Toyota"})
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def modelo(client: TestClient, marca: dict) -> dict:
    resp = client.post("/modelos/", json={
        "marca_id": marca["id"],
        "nome": "Corolla",
        "valor_fipe": 120000.00,
    })
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture
def carro(client: TestClient, modelo: dict) -> dict:
    resp = client.post("/carros/", json={
        "modelo_id": modelo["id"],
        "ano": 2022,
        "combustivel": "Flex",
        "num_portas": 4,
        "cor": "Prata",
        "quilometragem": 15000.0,
        "valor_anuncio": 115000.00,
    })
    assert resp.status_code == 201
    return resp.json()
