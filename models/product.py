from pydantic import BaseModel

class Product(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int