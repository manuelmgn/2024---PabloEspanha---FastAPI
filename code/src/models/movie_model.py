import datetime
from pydantic import BaseModel, Field, validator


class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str


class MovieCreate(BaseModel):
    id: int
    title: str
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

    @validator('title')
    def validate_title(cls, value):
        if len(value) < 5:
            raise ValueError('El título debe tener como mínimo 5 caracteres')
        if len(value) > 30:
            raise ValueError('El título debe tener como máximo 30 caracteres')
        return value  # Aquí se devuelve el valor tras la validación


class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str
