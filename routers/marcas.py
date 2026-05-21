import uuid
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.marcas import Marca, MarcaCreate, MarcaRead, MarcaUpdate

router = APIRouter(prefix="/marcas")
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/", response_model=List[MarcaRead], summary="Listar todas")
def list_marcas(session: SessionDep):
    return session.exec(select(Marca)).all()


@router.get("/{marca_id}", response_model=MarcaRead, summary="Buscar por ID", description="Retorna o objeto ou 404 - Not Found")
def get_marca(marca_id: uuid.UUID, session: SessionDep):
    marca = session.get(Marca, marca_id)
    if not marca:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    return marca


@router.post("/", response_model=MarcaRead, status_code=201)
def create_marca(marca_in: MarcaCreate, session: SessionDep):
    marca = Marca.model_validate(marca_in)
    session.add(marca)
    session.commit()
    session.refresh(marca)
    return marca


@router.put("/{marca_id}", response_model=MarcaRead)
def update_marca(
    marca_id: uuid.UUID, marca_in: MarcaUpdate, session: SessionDep
):
    marca = session.get(Marca, marca_id)
    if not marca:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    data = marca_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(marca, key, value)
    session.add(marca)
    session.commit()
    session.refresh(marca)
    return marca


@router.delete("/{marca_id}", status_code=204)
def delete_marca(marca_id: uuid.UUID, session: SessionDep):
    marca = session.get(Marca, marca_id)
    if marca:
        session.delete(marca)
        session.commit()
