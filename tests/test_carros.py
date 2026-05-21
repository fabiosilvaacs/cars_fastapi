"""
Testes CRUD completos para o recurso /carros.
"""
import uuid
import pytest
from fastapi.testclient import TestClient


CARRO_BASE = {
    "ano": 2022,
    "combustivel": "Flex",
    "num_portas": 4,
    "cor": "Prata",
    "quilometragem": 15000.0,
    "valor_anuncio": 115000.00,
}


class TestListCarros:
    def test_lista_vazia(self, client: TestClient):
        resp = client.get("/carros/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_lista_com_registros(self, client: TestClient, carro: dict):
        resp = client.get("/carros/")
        assert resp.status_code == 200
        assert len(resp.json()) == 1


class TestGetCarro:
    def test_busca_por_id_existente(self, client: TestClient, carro: dict):
        resp = client.get(f"/carros/{carro['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == carro["id"]
        assert data["cor"] == "Prata"
        assert data["ano"] == 2022

    def test_busca_por_id_inexistente_retorna_404(self, client: TestClient):
        resp = client.get(f"/carros/{uuid.uuid4()}")
        assert resp.status_code == 404
        assert "não encontrado" in resp.json()["detail"]

    def test_id_invalido_retorna_422(self, client: TestClient):
        resp = client.get("/carros/abc")
        assert resp.status_code == 422


class TestCreateCarro:
    def test_cria_carro_com_sucesso(self, client: TestClient, modelo: dict):
        payload = {**CARRO_BASE, "modelo_id": modelo["id"]}
        resp = client.post("/carros/", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["modelo_id"] == modelo["id"]
        assert data["ano"] == 2022
        assert data["combustivel"] == "Flex"
        assert "id" in data
        assert "timestamp_cadastro" in data

    def test_cria_carro_com_descricao_opcional(self, client: TestClient, modelo: dict):
        payload = {**CARRO_BASE, "modelo_id": modelo["id"], "descricao": "Único dono, revisado"}
        resp = client.post("/carros/", json=payload)
        assert resp.status_code == 201
        assert resp.json()["descricao"] == "Único dono, revisado"

    def test_cria_carro_sem_descricao_nao_inclui_campo_none(self, client: TestClient, modelo: dict):
        payload = {**CARRO_BASE, "modelo_id": modelo["id"]}
        resp = client.post("/carros/", json=payload)
        assert resp.status_code == 201
        # NoneExcludedResponse não deve retornar a chave "descricao"
        assert "descricao" not in resp.json()

    def test_cria_carro_com_modelo_inexistente_retorna_404(self, client: TestClient):
        payload = {**CARRO_BASE, "modelo_id": str(uuid.uuid4())}
        resp = client.post("/carros/", json=payload)
        assert resp.status_code == 404
        assert "Modelo" in resp.json()["detail"]

    def test_corpo_incompleto_retorna_422(self, client: TestClient, modelo: dict):
        resp = client.post("/carros/", json={"modelo_id": modelo["id"], "ano": 2022})
        assert resp.status_code == 422

    def test_corpo_vazio_retorna_422(self, client: TestClient):
        resp = client.post("/carros/", json={})
        assert resp.status_code == 422

    def test_cria_multiplos_carros(self, client: TestClient, modelo: dict):
        for cor in ["Vermelho", "Azul", "Branco"]:
            resp = client.post("/carros/", json={**CARRO_BASE, "modelo_id": modelo["id"], "cor": cor})
            assert resp.status_code == 201
        lista = client.get("/carros/").json()
        assert len(lista) == 3


class TestUpdateCarro:
    def test_atualiza_cor(self, client: TestClient, carro: dict):
        resp = client.put(f"/carros/{carro['id']}", json={"cor": "Preto"})
        assert resp.status_code == 200
        assert resp.json()["cor"] == "Preto"

    def test_atualiza_quilometragem_e_valor(self, client: TestClient, carro: dict):
        resp = client.put(f"/carros/{carro['id']}", json={
            "quilometragem": 20000.0,
            "valor_anuncio": 110000.00,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["quilometragem"] == 20000.0
        assert data["valor_anuncio"] == 110000.00

    def test_atualiza_descricao(self, client: TestClient, carro: dict):
        resp = client.put(f"/carros/{carro['id']}", json={"descricao": "Revisado em 2024"})
        assert resp.status_code == 200
        assert resp.json()["descricao"] == "Revisado em 2024"

    def test_atualiza_modelo_id_para_inexistente_retorna_404(self, client: TestClient, carro: dict):
        resp = client.put(f"/carros/{carro['id']}", json={"modelo_id": str(uuid.uuid4())})
        assert resp.status_code == 404

    def test_atualiza_carro_inexistente_retorna_404(self, client: TestClient):
        resp = client.put(f"/carros/{uuid.uuid4()}", json={"cor": "Rosa"})
        assert resp.status_code == 404

    def test_update_preserva_campos_nao_enviados(self, client: TestClient, carro: dict):
        client.put(f"/carros/{carro['id']}", json={"cor": "Amarelo"})
        resp = client.get(f"/carros/{carro['id']}")
        data = resp.json()
        assert data["ano"] == 2022
        assert data["combustivel"] == "Flex"
        assert data["num_portas"] == 4


class TestDeleteCarro:
    def test_deleta_carro_existente(self, client: TestClient, carro: dict):
        resp = client.delete(f"/carros/{carro['id']}")
        assert resp.status_code == 204

    def test_carro_nao_existe_apos_delete(self, client: TestClient, carro: dict):
        client.delete(f"/carros/{carro['id']}")
        resp = client.get(f"/carros/{carro['id']}")
        assert resp.status_code == 404

    def test_deleta_id_inexistente_retorna_204(self, client: TestClient):
        resp = client.delete(f"/carros/{uuid.uuid4()}")
        assert resp.status_code == 204
