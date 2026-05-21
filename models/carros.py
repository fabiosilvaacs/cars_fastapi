import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class CarroBase(SQLModel):
    modelo_id: uuid.UUID = Field(foreign_key="modelo.id")
    ano: int
    combustivel: str
    num_portas: int
    cor: str
    quilometragem: float
    valor_anuncio: float
    descricao: Optional[str] = None


class Carro(CarroBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    timestamp_cadastro: datetime = Field(default_factory=datetime.utcnow)


class CarroCreate(CarroBase):
    pass


class CarroUpdate(SQLModel):
    modelo_id: Optional[uuid.UUID] = None
    ano: Optional[int] = None
    combustivel: Optional[str] = None
    num_portas: Optional[int] = None
    cor: Optional[str] = None
    quilometragem: Optional[float] = None
    valor_anuncio: Optional[float] = None
    descricao: Optional[str] = None


class CarroRead(CarroBase):
    id: uuid.UUID
    timestamp_cadastro: datetime
