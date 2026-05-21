import uuid
from typing import Optional
from sqlmodel import Field, SQLModel


class ModeloBase(SQLModel):
    marca_id: uuid.UUID = Field(foreign_key="marca.id")
    nome: str
    valor_fipe: float


class Modelo(ModeloBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )


class ModeloCreate(ModeloBase):
    pass


class ModeloUpdate(SQLModel):
    marca_id: Optional[uuid.UUID] = None
    nome: Optional[str] = None
    valor_fipe: Optional[float] = None


class ModeloRead(ModeloBase):
    id: uuid.UUID
