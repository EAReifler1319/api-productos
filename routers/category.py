from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.category import Categoria, CategoriaCreate, CategoriaUpdate
from models.product import Producto

router = APIRouter(prefix="/categorias", tags=["Categorías"])


# Crear una categoría
@router.post("/", response_model=Categoria, status_code=201)
def crear_categoria(datos: CategoriaCreate, session: Session = Depends(get_session)):
    categoria = Categoria.model_validate(datos)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


# Listar todas las categorías
@router.get("/", response_model=list[Categoria])
def listar_categorias(session: Session = Depends(get_session)):
    return session.exec(select(Categoria)).all()


# Consultar una categoría específica
@router.get("/{id}", response_model=Categoria)
def obtener_categoria(id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


# Actualizar una categoría
@router.put("/{id}", response_model=Categoria)
def actualizar_categoria(id: int, datos: CategoriaUpdate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    cambios = datos.model_dump(exclude_unset=True)
    categoria.sqlmodel_update(cambios)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


# Eliminar una categoría
@router.delete("/{id}")
def eliminar_categoria(id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    producto = session.exec(select(Producto).where(Producto.categoria_id == id)).first()
    if producto:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar: la categoría tiene productos asociados",
        )
    session.delete(categoria)
    session.commit()
    return {"mensaje": "Categoría eliminada"}