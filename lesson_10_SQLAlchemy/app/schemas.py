from pydantic import BaseModel


class FilmBase(BaseModel):
    title: str
    description: str | None = None


class FilmCreate(BaseModel):
    title: str
    year: int | None = None
    genre: str
    producer: str | None = None
    duration: str | None = None
    actors: str | None = None


class FilmUpdate(BaseModel):
    pass


class FilmResponse(FilmBase):
    id: int
    year: int | None = None
    producer: str | None = None
    duration: str | None = None
    actors: str | None = None
