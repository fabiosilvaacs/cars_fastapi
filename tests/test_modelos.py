"""
Testes CRUD completos para o recurso /modelos.
"""
import uuid
import pytest
from fastapi.testclient import TestClient


class TestListModelos:
    def test_lista_vazia(self, client: TestClient):
        resp = client.get("/modelos/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_lista_com_registros(self, client: TestClient, modelo: dict):
        resp = client.get("/modelos/")
        assert resp.status_code == 200
        assert len(resp.json()) == 1


class TestGetModelo:
    def test_busca_por_id_existente(self, client: TestClient, modelo: dict):
        resp = client.get(f"/modelos/{modelo['id']}")
        assert resp.status_code == 200
        assert resp.json()["nome"] == "Corolla"
        assert resp.json()["valor_fipe"] == 120000.00

    def test_busca_por_id_inexistente_retorna_404(self, client: TestClient):
        resp = client.get(f"/modelos/{uuid.uuid4()}")
        assert resp.status_code == 404
        assert "não encontrado" in resp.json()["detail"]

    def test_id_invalido_retorna_422(self, client: TestClient):
        resp = client.get("/modelos/abc")
        assert resp.status_code == 422


class TestCreateModelo:
    def test_cria_modelo_com_sucesso(self, client: TestClient, marca: dict):
        resp = client.post("/modelos/", json={
            "marca_id": marca["id"],
            "nome": "Civic",
            "valor_fipe": 130000.00,
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["nome"] == "Civic"
        assert data["marca_id"] == marca["id"]

    def test_cria_modelo_com_marca_inexistente_retorna_404(self, client: TestClient):
        resp = client.post("/modelos/", json={
            "marca_id": str(uuid.uuid4()),
            "nome": "Fantasma",
            "valor_fipe": 50000.00,
        })
        assert resp.status_code == 404
        assert "Marca" in resp.json()["detail"]

    def test_corpo_incompleto_retorna_422(self, client: TestClient, marca: dict):
        resp = client.post("/modelos/", json={"marca_id": marca["id"]})
        assert resp.status_code == 422

    def test_cria_varios_modelos_para_mesma_marca(self, client: TestClient, marca: dict):
        for nome, fipe in [("Yaris", 80000), ("Hilux", 200000), ("RAV4", 250000)]:
            resp = client.post("/modelos/", json={
                "marca_id": marca["id"],
                "nome": nome,
                "valor_fipe": fipe,
            })
            assert resp.status_code == 201
        lista = client.get("/modelos/").json()
        assert len(lista) == 3


class TestUpdateModelo:
    def test_atualiza_nome(self, client: TestClient, modelo: dict):
        resp = client.put(f"/modelos/{modelo['id']}", json={"nome": "Corolla Cross"})
        assert resp.status_code == 200
        assert resp.json()["nome"] == "Corolla Cross"

    def test_atualiza_valor_fipe(self, client: TestClient, modelo: dict):
        resp = client.put(f"/modelos/{modelo['id']}", json={"valor_fipe": 135000.00})
        assert resp.status_code == 200
        assert resp.json()["valor_fipe"] == 135000.00

    def test_atualiza_marca_id_para_inexistente_retorna_404(self, client: TestClient, modelo: dict):
        resp = client.put(f"/modelos/{modelo['id']}", json={"marca_id": str(uuid.uuid4())})
        assert resp.status_code == 404

    def test_atualiza_modelo_inexistente_retorna_404(self, client: TestClient):
        resp = client.put(f"/modelos/{uuid.uuid4()}", json={"nome": "X"})
        assert resp.status_code == 404

    def test_update_preserva_campos_nao_enviados(self, client: TestClient, modelo: dict):
        client.put(f"/modelos/{modelo['id']}", json={"nome": "Corolla Novo"})
        resp = client.get(f"/modelos/{modelo['id']}")
        assert resp.json()["valor_fipe"] == 120000.00  # não foi alterado


class TestDeleteModelo:
    def test_deleta_modelo_existente(self, client: TestClient, modelo: dict):
        resp = client.delete(f"/modelos/{modelo['id']}")
        assert resp.status_code == 204

    def test_modelo_nao_existe_apos_delete(self, client: TestClient, modelo: dict):
        client.delete(f"/modelos/{modelo['id']}")
        resp = client.get(f"/modelos/{modelo['id']}")
        assert resp.status_code == 404

    def test_deleta_id_inexistente_retorna_204(self, client: TestClient):
        resp = client.delete(f"/modelos/{uuid.uuid4()}")
        assert resp.status_code == 204
