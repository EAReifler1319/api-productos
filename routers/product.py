from fastapi import APIRouter, HTTPException
from models.product import Product

router = APIRouter(prefix="/productos", tags=["Productos"])

productos = []

# Ver todos los productos
@router.get("/")
def listar_productos():
    return productos

# Crear / agregar un producto
@router.post("/")
def crear_producto(producto: Product):
    for p in productos:
        if p.id == producto.id:
            raise HTTPException(status_code=400, detail="Ya existe un producto con ese id")
    productos.append(producto)
    return producto

# Editar un producto
@router.put("/{id}")
def editar_producto(id: int, producto: Product):
    for i, p in enumerate(productos):
        if p.id == id:
            productos[i] = producto
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Eliminar un producto
@router.delete("/{id}")
def eliminar_producto(id: int):
    for p in productos:
        if p.id == id:
            productos.remove(p)
            return {"mensaje": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")