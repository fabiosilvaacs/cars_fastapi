import uuid
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.carros import Carro, CarroCreate, CarroRead, CarroUpdate
from models.modelos import Modelo


router = APIRouter(prefix="/carros")
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/", response_model=List[CarroRead], summary="Listar todos")
def list_carros(session: SessionDep):
    return session.exec(select(Carro)).all()


@router.get("/{carro_id}", response_model=CarroRead, summary="Buscar por ID", description="Retorna o objeto ou 404 - Not Found")
def get_carro(carro_id: uuid.UUID, session: SessionDep):
    carro = session.get(Carro, carro_id)
    if not carro:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return carro


@router.post("/", response_model=CarroRead, status_code=201)
def create_carro(carro_in: CarroCreate, session: SessionDep):
    if not session.get(Modelo, carro_in.modelo_id):
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    carro = Carro.model_validate(carro_in)
    session.add(carro)
    session.commit()
    session.refresh(carro)
    return carro


@router.put("/{carro_id}", response_model=CarroRead)
def update_carro(
    carro_id: uuid.UUID, carro_in: CarroUpdate, session: SessionDep
):
    carro = session.get(Carro, carro_id)
    if not carro:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    if carro_in.modelo_id and not session.get(Modelo, carro_in.modelo_id):
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    data = carro_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(carro, key, value)
    session.add(carro)
    session.commit()
    session.refresh(carro)
    return carro


@router.delete("/{carro_id}", status_code=204)
def delete_carro(carro_id: uuid.UUID, session: SessionDep):
    carro = session.get(Carro, carro_id)
    if carro:
        session.delete(carro)
        session.commit()
