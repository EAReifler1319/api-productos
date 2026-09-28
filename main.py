import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlmodel import Session

from database import crear_tablas, get_session
from routers.category import router as categoria_router
from routers.product import router as producto_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta una vez al arrancar la API
    crear_tablas()
    yield


app = FastAPI(
    title="API Productos",
    description="CRUD de Productos y Categorías con FastAPI, desplegada en AWS EC2 con base de datos en Amazon RDS (PostgreSQL).",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(categoria_router)
app.include_router(producto_router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API de Productos funcionando. Documentación en /docs"}


@app.get("/salud/db", tags=["Salud"])
def verificar_base_de_datos(session: Session = Depends(get_session)):
    fila = session.connection().execute(
        text("SELECT current_database(), inet_server_addr(), version()")
    ).one()
    return {
        "estado": "conectado",
        "endpoint_rds": os.getenv("DB_HOST"),
        "base_de_datos": fila[0],
        "ip_privada_servidor_db": str(fila[1]),
        "version_postgres": fila[2],
    }