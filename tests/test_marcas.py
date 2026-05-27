"""
Testes CRUD completos para o recurso /marcas.
"""
import uuid
import pytest
from fastapi.testclient import TestClient


class TestListMarcas:
    def test_lista_vazia(self, client: TestClient):
        resp = client.get("/marcas/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_lista_com_registros(self, client: TestClient, marca: dict):
        resp = client.get("/marcas/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["nome_marca"] == "Toyota"


class TestGetMarca:
    def test_busca_por_id_existente(self, client: TestClient, marca: dict):
        resp = client.get(f"/marcas/{marca['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == marca["id"]
        assert resp.json()["nome_marca"] == "Toyota"

    def test_busca_por_id_inexistente_retorna_404(self, client: TestClient):
        resp = client.get(f"/marcas/{uuid.uuid4()}")
        assert resp.status_code == 404
        assert "não encontrada" in resp.json()["detail"]

    def test_id_invalido_retorna_422(self, client: TestClient):
        resp = client.get("/marcas/nao-e-um-uuid")
        assert resp.status_code == 422


class TestCreateMarca:
    def test_cria_marca_com_sucesso(self, client: TestClient):
        resp = client.post("/marcas/", json={"nome_marca": "Honda"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["nome_marca"] == "Honda"
        assert "id" in data

    def test_corpo_vazio_retorna_422(self, client: TestClient):
        resp = client.post("/marcas/", json={})
        assert resp.status_code == 422

    def test_cria_multiplas_marcas(self, client: TestClient):
        for nome in ["Fiat", "Ford", "Volkswagen"]:
            resp = client.post("/marcas/", json={"nome_marca": nome})
            assert resp.status_code == 201
        lista = client.get("/marcas/").json()
        assert len(lista) == 3

    def test_resposta_exclui_campos_none(self, client: TestClient):
        resp = client.post("/marcas/", json={"nome_marca": "BMW"})
        # NoneExcludedResponse não deve incluir chaves com valor None
        for value in resp.json().values():
            assert value is not None


class TestUpdateMarca:
    def test_atualiza_nome_com_sucesso(self, client: TestClient, marca: dict):
        resp = client.put(f"/marcas/{marca['id']}", json={"nome_marca": "Toyota Motors"})
        assert resp.status_code == 200
        assert resp.json()["nome_marca"] == "Toyota Motors"

    def test_atualiza_marca_inexistente_retorna_404(self, client: TestClient):
        resp = client.put(f"/marcas/{uuid.uuid4()}", json={"nome_marca": "X"})
        assert resp.status_code == 404

    def test_update_sem_body_retorna_200_sem_alteracao(self, client: TestClient, marca: dict):
        """PUT com payload vazio não altera nada (exclude_unset)."""
        resp = client.put(f"/marcas/{marca['id']}", json={})
        assert resp.status_code == 200
        assert resp.json()["nome_marca"] == "Toyota"


class TestDeleteMarca:
    def test_deleta_marca_existente(self, client: TestClient, marca: dict):
        resp = client.delete(f"/marcas/{marca['id']}")
        assert resp.status_code == 204

    def test_marca_nao_existe_apos_delete(self, client: TestClient, marca: dict):
        client.delete(f"/marcas/{marca['id']}")
        resp = client.get(f"/marcas/{marca['id']}")
        assert resp.status_code == 404

    def test_deleta_id_inexistente_retorna_404(self, client: TestClient):
        """Delete idempotente: mesmo sem encontrar, retorna 404."""
        resp = client.delete(f"/marcas/{uuid.uuid4()}")
        assert resp.status_code == 404
