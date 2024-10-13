# Notes

- [Intro](#intro)
  - [Instalación y configuración](#instalación-y-configuración)
  - [Primera app](#primera-app)
  - [Documentación](#documentación)
- [Path Operations](#path-operations)
  - [GET y parámetros](#get-y-parámetros)
  - [POST](#post)
  - [PUT](#put)
  - [DELETE](#delete)
- [Validación de datos](#validación-de-datos)
- [Tipos de respuestas y códigos de estados](#tipos-de-respuestas-y-códigos-de-estados)
- [Middlewares](#middlewares)
- [Dependencias](#dependencias)
- [Modularización](#modularización)
- [Manejo de errores](#manejo-de-errores)

## Intro

-   **FastAPI**: Framework moderno, rápido (de alto rendimiento) para construir APIs con Python 3.7+ basado en las anotaciones de tipos (_type hints_) de Python.
-   **Características**:
    -   **Basado en estándares**: OpenAPI (documentación), OAuth2 (integrado)...
    -   **Rápido**: Utiliza herramientas existentes, ya rápidas.
    -   **Contiene menos errores**, en parte gracias a las anotaciones de tipo.
    -   **Fácil e intuitivo**, en parte gracias a cómo es Python y a su documentación.
    -   **Robusto**.
-   Creado por Sebastián Ramírez 🇨🇴 en 2018.
-   Marco utilizado por FastAPI:
    -   **Starlette**: framework para desarrollo web, muy rápido. FastAPI se basa mucho en él.
    -   **Pydantic**. Encargado de los datos.
    -   **Uvicorn**. Ejecuta la aplicación.

### Instalación y configuración

-   Visual Studio Code (...)
-   Creación de entorno virtual: `python3.11 -m venv venv` (o `python3 -m venv venv`)
-   Activación del entorno: `source venv/bin/activate`
-   Instalamos fastapi y uvicorn: `pip install fastapi uvicorn`

Seleccionamos el intérprete de Python de VSC. Debe ser la misma que la del entorno que hemos instalado.

### Primera app

-   Creamos `main.py`
-   Importamos FastAPI
-   Inicializamos la app
-   Creamos la primera ruta, a /.
-   Función "home" para esta ruta que devuelva "Hola, mundo"
-   Ejecutamos con `uvicorn main:app`. Nos devuelve una URL donde podemos ver la aplicación.
    -   Si quieremos cambiar el puerto por defecto, ejecutaríamos `uvicorn main:app --port 5000`, por ejemplo.
    -   Para que el servidor se recargue automáticamente incluiremos `--reload`.
    -   Si queremos que la app se pueda ver desde toda la red local, usaremos `--host` con la ip `0.0.0.0`.
    -   `uvicorn main:app --host 0.0.0.0 --port 5000 --reload`

```py
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return "Hola, mundo!"
```

### Documentación

-   Se genera de manera automática, que describe cada uno de los _endpoints_, entre otras muchas cosas.
-   Podemos acceder a ella desde la url y `/docs`.
-   La documentación se puede modificar:
    -   Título, con `app.title`
    -   Versión, con `app.version`
    -   Tags. Podemos decir, por ejemplo, que el endpoint / pertenece a 'Home'. Si creamos otro endpoint con el mismo tag, la documentación de FastAPI los agrupará en el mismo epígrafe. ![doc-tags](img/doc-tags.png)
-   Si entramos en un endpoint, podemos ejecutarlo para ver cómo funciona directamente desde la documentación.

```py
from fastapi import FastAPI

app = FastAPI()

app.title = "Mi primera app con FastAPI"
app.version = "2.0.0"

@app.get('/', tags=['Home'])
def home():
    return "Hola, mundo!"

@app.get('/home', tags=['Home'])
def home():
    return "Hola, mundo!"
```

-   Hay otro tipo de documentación integrada: **redoc**. Se accede a través de `/redoc`.
-   Funciona de manera semejante.

## Path Operations

### GET y parámetros

#### GET

-   Con GET el cliente verá lo que devolvemos con el `return`, sea un _string_, un diccionario u otro tipo de dato.
    -   Un tipo de dato posible es HTML. Para ello, debemos importar este tipo de respuesta: `from fastapi.responses import HTMLResponse`.
    -   Después lo devolveríamos como `return HTMLResponse('<h1>Hello, world</h1>')`
-   Creamos una lista con diccionarios, uno por película.

```py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

movies = [
    {"id": 1,
    "title": "Avatar",
    "overview": "Bastante sobrevalorada",
    "year": "2009",
    "rating": 6.2,
    "category": "Acción"}
]

@app.get('/', tags=['Home'])
def home():
    return "Hola, mundo!"

@app.get('/movies', tags=['Home'])
def get_movies():
    return movies
```

#### Parámetros de ruta

-   Podemos usar **parámetros de rutas** desde una URL, lo hacemos con `{id}` en la ruta.
-   En la función, indicaremos que debemos recibir por parámetro una variable (id) de tipo int. `get_movie(id: int)`. De este modo, ya podremos acceder al parámetro.
-   En la función `get_movie` podemos recorrer las películas con `for` y, si el id de alguna coincide con el parámetro, le indicamos que devuelva esa película y, si no, una lista vacía.

```py
@app.get('/movies/{id}', tags=['Home'])
def get_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            return movie
    return []
```

#### Parámetros Query

-   En los parámetros de ruta usábamos la dirección, con la ruta y un parámetro específico, por ejemplo `http://localhost:5000/movies/1`. Los parámetros Query tienen otra estructura:
    -   Aquí, además del valor, debe ir su clave, es decir, el nombre del parámetro, `id=1`.
    -   Además, van precedidos del símbolo de interrogación `?`.
    -   `http://localhost:5000/movies/?id=1`
-   Son muy fáciles de definir, simplemente tenemos que hacerlo en la función y no en la URL.

    -   Si queremos usar una _query_ por categorías, su función podría ser `def get_movie_by_category(category: str)`. Es decir, definiendo aí la categoría y no en la ruta.

        ```py
        @app.get('/movies/', tags=['Home'])
        def get_movie_by_category(category: str):
            return category
        ```

        -   Por que `/movies/`, con la barra final? Porque ya teníamos definida la ruta `/movies` y porque en este caso tendrá algo a continuación de la barra: los parámetros query.

![Documentation - Query](img/doc-query.png)

-   Y si queremos añadir un segundo parámetro? Lo hacemos después del anterior, separados por una coma: `def get_movie_by_category(category: str, year: int)`.
-   En la documentación, al probar esta ruta, podremos ver la URL completa: 'http://127.0.0.1:8000/movies/?category=Comedia&year=2001'.
-   Podemos actualiza la función:

    ```py
    @app.get('/movies/', tags=['Home'])
    def get_movie_by_category(category: str, year: int):
        for movie in movies:
            if movie['category'] == category:
                return movie
        return []
    ```

![Documentation - Query test](img/docs-query-test.png)

### POST



### PUT

### DELETE

## Validación de datos

## Tipos de respuestas y códigos de estados

## Middlewares

## Dependencias

## Modularización

## Manejo de errores
