import uuid
from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from database import get_session
from exceptions import ConflictError, NotFoundError
from models.marcas import Marca
from models.modelos import Modelo, ModeloCreate, ModeloRead, ModeloUpdate
from models.carros import Carro

router = APIRouter(prefix="/modelos")
SessionDep = Annotated[Session, Depends(get_session)]


MARCA_NOT_FOUND = NotFoundError("Marca não encontrada")
MODELO_NOT_FOUND = NotFoundError("Modelo não encontrado")

@router.get("/", response_model=List[ModeloRead], summary="Listar todos")
def list_modelos(session: SessionDep):
    return session.exec(select(Modelo)).all()


@router.get("/{modelo_id}", response_model=ModeloRead, summary="Buscar por ID", description="Retorna o objeto ou 404 - Not Found")
def get_modelo(modelo_id: uuid.UUID, session: SessionDep):
    modelo = session.get(Modelo, modelo_id)
    if not modelo:
        raise MODELO_NOT_FOUND
    return modelo


@router.post("/", response_model=ModeloRead, status_code=201)
def create_modelo(modelo_in: ModeloCreate, session: SessionDep):
    if not session.get(Marca, modelo_in.marca_id):
        raise MARCA_NOT_FOUND
    modelo = Modelo.model_validate(modelo_in)
    session.add(modelo)
    session.commit()
    session.refresh(modelo)
    return modelo


@router.put("/{modelo_id}", response_model=ModeloRead)
def update_modelo(
    modelo_id: uuid.UUID, modelo_in: ModeloUpdate, session: SessionDep
):
    modelo = session.get(Modelo, modelo_id)
    if not modelo:
        raise MODELO_NOT_FOUND
    if modelo_in.marca_id and not session.get(Marca, modelo_in.marca_id):
        raise MARCA_NOT_FOUND
    data = modelo_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(modelo, key, value)
    session.add(modelo)
    session.commit()
    session.refresh(modelo)
    return modelo


@router.delete("/{modelo_id}", status_code=204)
def delete_modelo(modelo_id: uuid.UUID, session: SessionDep):
    modelo = session.get(Modelo, modelo_id)
    if not modelo:
        raise MODELO_NOT_FOUND

    # Contar carros que estão vinculados a esse modelo
    count_carros = session.exec(
        select(func.count(Carro.id)).where(Carro.modelo_id == modelo_id)
    ).first()

    if count_carros > 0:
        raise ConflictError("Modelo possui carros vinculados")

    session.delete(modelo)
    session.commit()
