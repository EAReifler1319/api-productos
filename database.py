import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlmodel import SQLModel, Session, create_engine

# Lee el archivo .env y carga sus valores como variables de entorno
load_dotenv()

# Verificamos que existan todas las variables necesarias
VARIABLES = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
faltantes = [v for v in VARIABLES if not os.getenv(v)]
if faltantes:
    raise RuntimeError(f"Faltan variables de entorno: {', '.join(faltantes)}")

# Construimos la URL de conexión a partir de las variables
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

# El engine administra las conexiones con la base
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def crear_tablas():
    """Crea en la base las tablas de todos los modelos con table=True."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Entrega una sesión por cada petición y la cierra al terminar."""
    with Session(engine) as session:
        yield session