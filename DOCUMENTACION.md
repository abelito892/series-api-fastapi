# __Práctica Página Web__

## Pasos realizados para completar la tarea

## Ejercicio 1. Añadir páginas web con Jinja2 a la API REST de la práctica anterior

Partimos de una aplicación FastApi ya funcional que se ejecuta mediante Docker Compose, usando MySQL como base de datos. Tiene páginas web renderizadas con Jinja2, un endpoint REST /`api/series` y un listado HTML `/series`. La base de datos se inicializa al arrancar la aplicación mediante `init_db()`. la aplicación no permitía crear series desde la interfaz web, solo crearlas.

## Objetivo del ejercicio

 Añadir una nueva página web que permita introducir una serie mediante un formulario html, guardar la serie en la base de datos MySQL y volver al listado de series una vez creadas.

 ## Resumen de los pasos realizados:

 * Se levantó la aplicación con Docker Compose, verificando que FastAPI y MySQL funcionaban correctamente.

* Se creó un entorno virtual (.venv) e instalaron las dependencias desde requirements.txt.

* Se añadió una nueva página web para crear series usando Jinja2.

* Se implementó una ruta GET para mostrar el formulario, y  una ruta POST para guardar la serie en la base de datos

* Se creó la plantilla HTML del formulario (serie_form.html).

* Se añadió un enlace de acceso al formulario desde la página principal.

* Se reconstruyó la imagen Docker para aplicar los cambios.

* Se comprobó que la nueva serie:

* aparece en el listado web

* aparece en la API REST

#### Aplicación levantada con Docker:
![Aplicación levantada con Docker:](image.png)

#### Página Principal:
![Página Principal](image-1.png)

#### Formulario añadir serie:
![Formulario añadir serie](image-2.png)

#### Envío del formmulario (antes de enviar y después)
![Formulario antes](image-3.png)
![añadí 3](image-4.png)

#### API REST:
![API REST](image-5.png)

## Ejercicio 2. Hacer que funcione con una base de datos mysql en localhost.

## Objetivo del ejercicio

La idea clave es que en local no existe fastapi-db, así que la conexión debe apuntar a localhost, sin romper Docker. Lo haremos a través de variables de entorno.

Lo primero será ver si MySQL está activo y escuchando en el puerto 3306 usando el comando `ss -lntp | grep 3306`, si no sale nada, necesitaremos arrancar MySQL o instalarlo.
Una vez comprobado, ya sabemos que está escuchando por ese puerto y pasaremos a realizar una configuración correcta de `DB_URL`, aunque el `/src/data/db.py` ya está preparado porque está usando ` engine = create_engine(os.getenv("DB_URL", DATABASE_URL), echo=True) ` por lo que escribimos en la terminal export DB_URL="mysql+pymysql://quevedo:1234@localhost:3306/seriesdb", aunque en caso de ser powershell en vez de export sería `$env:DB_URL=` y lo que sigue a continuación que sería igual que en el bash. 

Y arrancamos la aplicación.

![Arranque de la aplicación](image-6.png)

![Localhost:9000/series](image-7.png)

## Ejercicio 3. Hacer que funcione con una base de datos mysql en un contenedor y la app en otro.

Este paso se puede comprobar en el ejercicio 1, que usamos un docker-compose con fastapi-app + fastapi-db, por lo tanto pasamos al siguiente ejercicio.

Aunque proporcionaré una serie de capturas que demuestran que se desplegó de esa manera, antes de hacerlo para este ejercicio.

### Docker-compose funcionando
![docker compose funcionando](image-8.png)

![Página en el navegador como localhost:8000/series/nueva](image-9.png)

## Ejercicio 4. PostgreSQL en lugar de MySQL

Lo primero que vamos a hacer es cambiar dependencias en requirements.txt. sustituyendo pymysql por el driver de Postgres. En requirements.txt eliminamos, o dejamos, realmente no afecta: pymysql, pero añadimos: `psycopg2-binary` que es un driver específico que necesita el motor de postgreSQL.

![requirements.txt con el nuevo psycopg2-binary](image-10.png)

A continuación, cambiamos la  conexión en src/data/db.py, cambiando a Postgres:
```db_user: str = "quevedo"
db_password: str = "1234"
db_server: str = "fastapi-pg"
db_port: int = 5432
db_name: str = "seriesdb" 
```
Y el URL quedaría de esta manera:

`DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(os.getenv("DB_URL", DATABASE_URL), echo=True)`

Pasamos a arrancar docker-compose:

![docker compose up](image-11.png)

![docker ps](image-12.png)


![ventanas del navegador escuchando en el puerto 8001 ](image-13.png)

## Nota: Este ejercicio lo he hecho con ayuda de la IA ` 

## Ejercicio 5. 