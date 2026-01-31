from datetime import date
from sqlmodel import Field, SQLModel

class Serie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, max_length=50)
    fecha_estreno: date | None = Field(nullable=True)

