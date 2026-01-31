from sqlmodel import create_engine, SQLModel, Session
from models.serie import Serie
import os

db_user: str = "quevedo"
db_password: str = "1234"
db_server: str = "fastapi-pg"   # nombre del servicio postgres en docker-compose
db_port: int = 5432
db_name: str = "seriesdb"

DATABASE_URL = (
    f"postgresql+psycopg2://{db_user}:{db_password}"
    f"@{db_server}:{db_port}/{db_name}"
)

engine = create_engine(
    os.getenv("DB_URL", DATABASE_URL),
    echo=True
)


def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Serie(id=1, nombre="The Mandalorian", fecha_estreno="2023-09-10"))
        session.add(Serie(id=2, nombre="The Simpsons", fecha_estreno="2024-03-20"))
        session.add(Serie(id=3, nombre="Friends", fecha_estreno="2019-02-22"))
        session.add(Serie(id=4, nombre="House of dragon", fecha_estreno="2021-10-01"))
        session.add(Serie(id=5, nombre="Lord of the rings", fecha_estreno="2023-09-10"))
        session.commit()
        #session.refresh_all()

