from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.category import Categoria
from models.product import Producto, ProductoCreate, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["Productos"])


def validar_categoria(session: Session, categoria_id: int):
    if not session.get(Categoria, categoria_id):
        raise HTTPException(status_code=404, detail="La categoría indicada no existe")


# Crear un producto
@router.post("/", response_model=Producto, status_code=201)
def crear_producto(datos: ProductoCreate, session: Session = Depends(get_session)):
    validar_categoria(session, datos.categoria_id)
    producto = Producto.model_validate(datos)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


# Listar productos (opcionalmente filtrados por categoría)
@router.get("/", response_model=list[Producto])
def listar_productos(categoria_id: Optional[int] = None, session: Session = Depends(get_session)):
    consulta = select(Producto)
    if categoria_id is not None:
        consulta = consulta.where(Producto.categoria_id == categoria_id)
    return session.exec(consulta).all()


# Consultar un producto específico
@router.get("/{id}", response_model=Producto)
def obtener_producto(id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


# Actualizar un producto
@router.put("/{id}", response_model=Producto)
def actualizar_producto(id: int, datos: ProductoUpdate, session: Session = Depends(get_session)):
    producto = session.get(Producto, id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    cambios = datos.model_dump(exclude_unset=True)
    if "categoria_id" in cambios:
        validar_categoria(session, cambios["categoria_id"])
    producto.sqlmodel_update(cambios)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


# Eliminar un producto
@router.delete("/{id}")
def eliminar_producto(id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return {"mensaje": "Producto eliminado"}