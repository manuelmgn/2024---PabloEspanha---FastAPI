from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse

from src.routers.movie_router import movie_router

app = FastAPI()


@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content='Home', status_code=200)


app.include_router(prefix='/movies', router=movie_router)
