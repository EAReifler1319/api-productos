from typing import Optional
from sqlmodel import SQLModel, Field


class ProductoBase(SQLModel):
    nombre: str = Field(max_length=150)
    precio: float = Field(ge=0)
    stock: int = Field(ge=0)
    categoria_id: int = Field(foreign_key="categoria.id")


class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=150)
    precio: Optional[float] = Field(default=None, ge=0)
    stock: Optional[int] = Field(default=None, ge=0)
    categoria_id: Optional[int] = None