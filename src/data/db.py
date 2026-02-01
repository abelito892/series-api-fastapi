from sqlmodel import create_engine, SQLModel, Session
from models.serie import Serie
import os

# 1. Intentamos obtener la URL de Render (DATABASE_URL)
# Si no existe (estás en local), usamos la de Docker por defecto
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Este pequeño truco es necesario porque Render a veces usa "postgres://" 
    # y SQLAlchemy requiere "postgresql://" para funcionar
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    # Esta es tu configuración original para Docker/Local
    db_user = "quevedo"
    db_password = "1234"
    db_server = "fastapi-pg" 
    db_port = 5432
    db_name = "seriesdb"
    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"

# Creamos el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    # ATENCIÓN: drop_all borrará los datos cada vez que la app se reinicie.
    # Úsalo solo al principio. Luego podrías comentarlo.
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Solo añadimos si quieres datos de prueba iniciales
        session.add(Serie(id=1, nombre="The Mandalorian", fecha_estreno="2023-09-10"))
        session.add(Serie(id=2, nombre="The Simpsons", fecha_estreno="2024-03-20"))
        session.add(Serie(id=3, nombre="Friends", fecha_estreno="2019-02-22"))
        session.add(Serie(id=4, nombre="House of dragon", fecha_estreno="2021-10-01"))
        session.add(Serie(id=5, nombre="Lord of the rings", fecha_estreno="2023-09-10"))
        session.commit()