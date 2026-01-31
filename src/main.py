from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import Depends
from sqlmodel import Session, select
from data.db import init_db, get_session
from models.serie import Serie

# -------------------------------
# IMPORTS AÑADIDOS PARA EL EJERCICIO
# -------------------------------
from fastapi import Form                     # Para recoger datos de formularios HTML
from fastapi.responses import RedirectResponse  # Para redirigir tras el POST
from datetime import date                    # Para convertir la fecha del formulario

import uvicorn


@asynccontextmanager
async def lifespan(application: FastAPI):
    # Se ejecuta al arrancar la aplicación
    init_db()
    yield


# Dependencia para inyectar la sesión de base de datos
SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)


# Configuración de archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# =========================
# PÁGINAS WEB
# =========================
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    mensaje = "Hola mundo"
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "mensaje": mensaje}
    )


@app.get("/series", response_class=HTMLResponse)
async def ver_series(request: Request, session: SessionDep):
    series = session.exec(select(Serie)).all()
    return templates.TemplateResponse(
        "series.html",
        {"request": request, "series": series}
    )


# ------------------------------------------------
# NUEVA PÁGINA: FORMULARIO PARA AÑADIR SERIE (GET)
# ------------------------------------------------
@app.get("/series/nueva", response_class=HTMLResponse)
async def formulario_nueva_serie(request: Request):
    # Muestra el formulario HTML para crear una nueva serie
    return templates.TemplateResponse(
        "serie_form.html",
        {"request": request, "error": None}
    )


# ------------------------------------------------
# NUEVA FUNCIÓN: PROCESAR FORMULARIO (POST)
# ------------------------------------------------
@app.post("/series/nueva")
async def crear_serie(
    request: Request,
    session: SessionDep,
    nombre: str = Form(...),          # Campo obligatorio del formulario
    fecha_estreno: str = Form(None)   # Campo opcional del formulario
):
    # Eliminamos espacios en blanco
    nombre = nombre.strip()

    # Validación básica: el nombre no puede estar vacío
    if not nombre:
        return templates.TemplateResponse(
            "serie_form.html",
            {
                "request": request,
                "error": "El nombre no puede estar vacío"
            }
        )

    # Convertimos la fecha (si se ha introducido)
    fecha: date | None = None
    if fecha_estreno:
        fecha = date.fromisoformat(fecha_estreno)

    # Creamos el objeto Serie
    nueva_serie = Serie(
        nombre=nombre,
        fecha_estreno=fecha
    )

    # Guardamos en base de datos
    session.add(nueva_serie)
    session.commit()

    # Redirigimos al listado de series (patrón POST-Redirect-GET)
    return RedirectResponse(
        url="/series",
        status_code=303
    )


@app.get("/series/{serie_id}", response_class=HTMLResponse)
async def buscar_serie_por_id(
    serie_id: int,
    request: Request,
    session: SessionDep
):
    serie_encontrada = session.get(Serie, serie_id)
    if not serie_encontrada:
        raise HTTPException(status_code=404, detail="Serie no encontrada")

    return templates.TemplateResponse(
        "serie_detalle.html",
        {"request": request, "serie": serie_encontrada}
    )


# =========================
# SERVICIOS WEB REST
# =========================
@app.get("/api/series", response_model=list[Serie])
async def lista_series(session: SessionDep):
    series = session.exec(select(Serie)).all()
    return series


'''
TODO LO QUE HAY AQUÍ COMENTADO
SE QUEDA TAL CUAL
NO SE TOCA
'''


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=3000,
        reload=True
    )
