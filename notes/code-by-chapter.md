# Code by chapter

- [CRUD y Path Operations](#crud-y-path-operations)
- [Validación de datos](#validación-de-datos)
- [Tipos de respuestas y códigos de estados](#tipos-de-respuestas-y-códigos-de-estados)
  - [Respuesta JSONResponse](#respuesta-jsonresponse)
  - [Resto de tipos de respuesta](#resto-de-tipos-de-respuesta)
  - [Códigos de estado](#códigos-de-estado)
- [Modularización](#modularización)

## CRUD y Path Operations

```py
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse


app = FastAPI()

movies = [
    {
        "id": 1,
        "title": "The Substance",
        "overview": "'Tú, pero mejor en todos los sentidos'",
        "year": "2024",
        "rating": 7.2,
        "category": "Ciencia Ficción"
    },
    {
        "id": 2,
        "title": "The Fall: El sueño de Alexandria",
        "overview": "Hollywood, años veinte. Tras una desafortunada caída, un especialista en secuencias de acción es ingresado en un hospital",
        "year": "2006",
        "rating": 7.0,
        "category": "Fantástico"
    },
    {
        "id": 3,
        "title": "Aftersun",
        "overview": "Sophie reflexiona sobre la alegría compartida y la melancolía privada de unas vacaciones que hizo con su padre 20 años atrás",
        "year": "2022",
        "rating": 7.2,
        "category": "Drama"
    }
]


@app.get('/', tags=['Home'])
def home():
    return "Hola, mundo!"


@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies


@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            return movie
    return []


@app.get('/movies/', tags=['Movies'])
def get_movie_by_category(category: str, year: int):
    for movie in movies:
        if movie['category'] == category:
            return movie
    return []


@app.post('/movies', tags=['Movies'])
def create_movie(
    id: int = Body(),
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()
    ):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    })
    return movies

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(
    id: int,
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()
    ):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = title,
            movie['overview'] = overview,
            movie['year'] = year,
            movie['rating'] = rating,
            movie['category'] = category
    return movies

@app.delete('/movies/{id}', tags=['Movies'])
def get_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return movies
```

## Validación de datos

```py
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List

import datetime

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str

class MovieCreate(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=15, max_length=100)
    year: int = Field(le=datetime.date.today().year, gt=1880)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=50)

    model_config = {
        'json_schema_extra': {
            'example': {
                'id': 1,
                'title': "Título por defecto",
                'overview': "Overview por defecto",
                'year': 1900,
                'rating': 5.0,
                'category': "Ninguna"
            }
        }
    }

class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


movies: List[Movie] = []

@app.get('/', tags=['Home'])
def home():
    return "Hola, mundo!"


@app.get('/movies', tags=['Movies'])
def get_movies() -> List[Movie]:
    return [movie.model_dump() for movie in movies]


@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return movie.model_dump()
    return {}


@app.get('/movies/', tags=['Movies'])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return movie.model_dump()
    return {}


@app.post('/movies', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)
    return [movie.model_dump() for movie in movies]


@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    return [movie.model_dump() for movie in movies]


@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    return [movie.model_dump() for movie in movies]
```

## Tipos de respuestas y códigos de estados

### Respuesta JSONResponse

```py
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

import datetime

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str

class MovieCreate(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=15, max_length=100)
    year: int = Field(le=datetime.date.today().year, gt=1880)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=50)

    model_config = {
        'json_schema_extra': {
            'example': {
                'id': 1,
                'title': "Título por defecto",
                'overview': "Overview por defecto",
                'year': 1900,
                'rating': 5.0,
                'category': "Ninguna"
            }
        }
    }

class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


movies: List[Movie] = []

@app.get('/', tags=['Home'])
def home():
    return "Hola, mundo!"


@app.get('/movies', tags=['Movies'])
def get_movies() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)


@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content = movie.model_dump())
    return JSONResponse(content ={})


@app.get('/movies/', tags=['Movies'])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(content = movie.model_dump())
    return JSONResponse(content ={})


@app.post('/movies', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)


@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)


@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)
```

### Resto de tipos de respuesta

```py
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List

import datetime

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str

class MovieCreate(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=15, max_length=100)
    year: int = Field(le=datetime.date.today().year, gt=1880)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=50)

    model_config = {
        'json_schema_extra': {
            'example': {
                'id': 1,
                'title': "Título por defecto",
                'overview': "Overview por defecto",
                'year': 1900,
                'rating': 5.0,
                'category': "Ninguna"
            }
        }
    }

class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


movies: List[Movie] = []

@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content='Home')


@app.get('/movies', tags=['Movies'])
def get_movies() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)


@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content = movie.model_dump())
    return JSONResponse(content ={})


@app.get('/movies/', tags=['Movies'])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(content = movie.model_dump())
    return JSONResponse(content ={})


@app.post('/movies', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)
    # return RedirectResponse('/movies', status_code=303)


@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)


@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)

@app.get('/get_file')
def get_file():
    return FileResponse('archivo_prueba.txt')
```

### Códigos de estado

```py
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List

import datetime

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str

class MovieCreate(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=15, max_length=100)
    year: int = Field(le=datetime.date.today().year, gt=1880)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=50)

    model_config = {
        'json_schema_extra': {
            'example': {
                'id': 1,
                'title': "Título por defecto",
                'overview': "Overview por defecto",
                'year': 1900,
                'rating': 5.0,
                'category': "Ninguna"
            } 
        }
    }

class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


movies: List[Movie] = []

@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content='Home', status_code=200)


@app.get('/movies', tags=['Movies'], status_code=500, response_description="Nos debe devolver una respuesta exitosa")
def get_movies() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content = movie.model_dump(), status_code=200)
    return JSONResponse(content ={}, status_code=404)


@app.get('/movies/', tags=['Movies'])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(content = movie.model_dump(), status_code=200)
    return JSONResponse(content ={}, status_code=404)


@app.post('/movies', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=201)


@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

```

## Modularización

main.py:

```py
from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse

from src.routers.movie_router import movie_router

app = FastAPI()


@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content='Home', status_code=200)


app.include_router(prefix='/movies', router=movie_router)

```

movie_router.py:

```py
from fastapi.responses import JSONResponse
from fastapi import Path, Query, APIRouter
from typing import List, Optional
from src.models.movie_model import Movie, MovieCreate, MovieUpdate

movies: List[Movie] = []

movie_router = APIRouter()


@movie_router.get('/', tags=['Movies'], status_code=200, response_description="Nos debe devolver una respuesta exitosa")
def get_movies() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@movie_router.get('/{id}', tags=['Movies'])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)


@movie_router.get('/by_category', tags=['Movies'])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)


@movie_router.post('/', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=201)


@movie_router.put('/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@movie_router.delete('/{id}', tags=['Movies'])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

```

movie_model.py:

```py
from fastapi.responses import JSONResponse
from fastapi import Path, Query, APIRouter
from typing import List, Optional
from src.models.movie_model import Movie, MovieCreate, MovieUpdate

movies: List[Movie] = []

movie_router = APIRouter()


@movie_router.get('/', tags=['Movies'], status_code=200, response_description="Nos debe devolver una respuesta exitosa")
def get_movies() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@movie_router.get('/{id}', tags=['Movies'])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)


@movie_router.get('/by_category', tags=['Movies'])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)


@movie_router.post('/', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=201)


@movie_router.put('/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@movie_router.delete('/{id}', tags=['Movies'])
def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

```