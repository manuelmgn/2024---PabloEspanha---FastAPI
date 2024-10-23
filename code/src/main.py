from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse, PlainTextResponse

from routers.movie_router import movie_router
# from utils.http_error_handler import HTTPErrorHandler

app = FastAPI()


# app.add_middleware(HTTPErrorHandler)
@app.middleware("http")
async def http_error_handler(
    request: Request, call_next
) -> Response | JSONResponse:
    try:
        print("El middleware funciona!!")
        return await call_next(request)
    except Exception as e:
        content = f"exc: {str(e)}"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content=content, status_code=status_code)


@app.get("/", tags=["Home"])
def home():
    return PlainTextResponse(content="Home", status_code=200)


app.include_router(prefix="/movies", router=movie_router)
