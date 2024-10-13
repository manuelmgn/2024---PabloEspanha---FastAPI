# Notes

- [Intro](#intro)
  - [Instalación y configuración](#instalación-y-configuración)
  - [Primera app](#primera-app)
  - [Documentación](#documentación)
- [Path Operations](#path-operations)
  - [GET](#get)
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

@app.get('/' tags=['Home'])
def home():
    return "Hola, mundo!"

@app.get('/home' tags=['Home'])
def home():
    return "Hola, mundo!"
```

- Hay otro tipo de documentación integrada: **redoc**. Se accede a través de `/redoc`.
- Funciona de manera semejante.

## Path Operations

### GET

- Con GET el cliente verá lo que devolvemos con el `return`, sea un *string*, un diccionario u otro tipo de dato.

### POST

### PUT

### DELETE

## Validación de datos

## Tipos de respuestas y códigos de estados

## Middlewares

## Dependencias

## Modularización

## Manejo de errores