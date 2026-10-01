from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Film
from ..schemas import FilmCreate, FilmUpdate


def create_film(session:Session, payload: FilmCreate):
	film = Film(**payload.model_dump())
	session.add(film)
	session.commit()
	session.refresh(film)
	return film

def get_films(session:Session):
    stmt = select(Film)
    return list(session.scalars(stmt).all())