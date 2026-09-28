from typing import Optional
from sqlmodel import SQLModel, Field


class CategoriaBase(SQLModel):
    nombre: str = Field(max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=255)


class Categoria(CategoriaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=255)