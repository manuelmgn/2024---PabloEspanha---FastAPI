from fastapi import FastAPI, Body
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
def get_movies() -> List[Movie]:
    return [Movie(**movie).model_dump() for movie in movies]  # Convertimos los diccionarios a instancias de Movie


@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int) -> Movie:
    for movie in movies:
        if movie['id'] == id:
            return Movie(**movie).model_dump()  # Convertimos a instancia de Movie antes de llamar a model_dump()
    return []


@app.get('/movies/', tags=['Movies'])
def get_movie_by_category(category: str, year: int) -> Movie:
    for movie in movies:
        if movie['category'] == category:
            return Movie(**movie).model_dump()
    return []


@app.post('/movies', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie.dict())  # Agregamos el nuevo objeto como un diccionario
    return [Movie(**movie).model_dump() for movie in movies]


@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return [Movie(**movie).model_dump() for movie in movies]


@app.delete('/movies/{id}', tags=['Movies'])
def get_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return [Movie(**movie).model_dump() for movie in movies]