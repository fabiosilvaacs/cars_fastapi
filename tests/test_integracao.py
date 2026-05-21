"""
Testes de integração e comportamentos gerais da API.
"""
import pytest
from fastapi.testclient import TestClient


class TestRoot:
    def test_root_retorna_200(self, client: TestClient):
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json() == {"message": "API de Carros funcionando!"}


class TestNoneExcludedResponse:
    """Valida que a resposta global NoneExcludedResponse oculta campos None."""

    def test_carro_sem_descricao_nao_tem_chave_descricao(self, client: TestClient, modelo: dict):
        resp = client.post("/carros/", json={
            "modelo_id": modelo["id"],
            "ano": 2021,
            "combustivel": "Gasolina",
            "num_portas": 2,
            "cor": "Cinza",
            "quilometragem": 5000.0,
            "valor_anuncio": 90000.00,
        })
        assert "descricao" not in resp.json()

    def test_carro_com_descricao_tem_chave_descricao(self, client: TestClient, modelo: dict):
        resp = client.post("/carros/", json={
            "modelo_id": modelo["id"],
            "ano": 2021,
            "combustivel": "Gasolina",
            "num_portas": 2,
            "cor": "Cinza",
            "quilometragem": 5000.0,
            "valor_anuncio": 90000.00,
            "descricao": "Impecável",
        })
        assert resp.json()["descricao"] == "Impecável"


class TestFluxoCompleto:
    """Testa o fluxo Marca → Modelo → Carro de ponta a ponta."""

    def test_crud_completo(self, client: TestClient):
        # 1. Cria marca
        r = client.post("/marcas/", json={"nome_marca": "Chevrolet"})
        assert r.status_code == 201
        marca_id = r.json()["id"]

        # 2. Cria modelo
        r = client.post("/modelos/", json={
            "marca_id": marca_id,
            "nome": "Onix",
            "valor_fipe": 75000.00,
        })
        assert r.status_code == 201
        modelo_id = r.json()["id"]

        # 3. Cria carro
        r = client.post("/carros/", json={
            "modelo_id": modelo_id,
            "ano": 2023,
            "combustivel": "Flex",
            "num_portas": 4,
            "cor": "Branco",
            "quilometragem": 0.0,
            "valor_anuncio": 78000.00,
        })
        assert r.status_code == 201
        carro_id = r.json()["id"]

        # 4. Lê o carro
        r = client.get(f"/carros/{carro_id}")
        assert r.status_code == 200
        assert r.json()["cor"] == "Branco"

        # 5. Atualiza o carro
        r = client.put(f"/carros/{carro_id}", json={"quilometragem": 500.0})
        assert r.status_code == 200
        assert r.json()["quilometragem"] == 500.0

        # 6. Deleta o carro
        r = client.delete(f"/carros/{carro_id}")
        assert r.status_code == 204

        # 7. Deleta o modelo
        r = client.delete(f"/modelos/{modelo_id}")
        assert r.status_code == 204

        # 8. Deleta a marca
        r = client.delete(f"/marcas/{marca_id}")
        assert r.status_code == 204

        # 9. Confirma que tudo foi removido
        assert client.get(f"/carros/{carro_id}").status_code == 404
        assert client.get(f"/modelos/{modelo_id}").status_code == 404
        assert client.get(f"/marcas/{marca_id}").status_code == 404

    def test_modelo_herda_marca_id_corretamente(self, client: TestClient, marca: dict):
        r = client.post("/modelos/", json={
            "marca_id": marca["id"],
            "nome": "Etios",
            "valor_fipe": 60000.00,
        })
        assert r.json()["marca_id"] == marca["id"]

    def test_carro_herda_modelo_id_corretamente(self, client: TestClient, modelo: dict):
        r = client.post("/carros/", json={
            "modelo_id": modelo["id"],
            "ano": 2020,
            "combustivel": "Diesel",
            "num_portas": 4,
            "cor": "Verde",
            "quilometragem": 80000.0,
            "valor_anuncio": 95000.00,
        })
        assert r.json()["modelo_id"] == modelo["id"]

    def test_isolamento_entre_testes(self, client: TestClient):
        """Cada teste começa com banco vazio — sem vazamento de dados."""
        assert client.get("/marcas/").json() == []
        assert client.get("/modelos/").json() == []
        assert client.get("/carros/").json() == []
