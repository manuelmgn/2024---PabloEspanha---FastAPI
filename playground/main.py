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