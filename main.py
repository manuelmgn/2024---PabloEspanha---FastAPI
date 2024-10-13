from fastapi import FastAPI

app = FastAPI()

@app.get('/' tags=['Home'])
def home():
    return "Hola, mundo!"

@app.get('/movies' tags=['Home'])
def home():
    return "Hola, mundo!"