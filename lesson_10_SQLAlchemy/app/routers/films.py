from fastapi import APIRouter, status, HTTPException
from ..dependencies import SessionDep
from sqlalchemy.exc import IntegrityError

from ..schemas import FilmResponse, FilmCreate
from ..services import task_service


router = APIRouter(prefix="/films", tags=["films"])


@router.post("/", response_model=FilmResponse, status_code=status.HTTP_201_CREATED)
def creat_film(payload: FilmCreate, db: SessionDep):
    try:
        return task_service.create_film(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Creation error")


@router.get("/", response_model=list[FilmResponse])
def red_task(db: SessionDep):
    return task_service.get_films(db)
