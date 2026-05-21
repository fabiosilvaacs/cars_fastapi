import uuid
from typing import Optional
from sqlmodel import Field, SQLModel


class MarcaBase(SQLModel):
    nome_marca: str = Field(index=True)


class Marca(MarcaBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )


class MarcaCreate(MarcaBase):
    pass


class MarcaUpdate(SQLModel):
    nome_marca: Optional[str] = None


class MarcaRead(MarcaBase):
    id: uuid.UUID
