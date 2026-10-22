from fastapi import APIRouter, status, HTTPException
from sqlalchemy.exc import IntegrityError

from ..services import car_services
from .. import shemas
from ..dependencies import SessionDep

router = APIRouter(prefix="/cars", tags=["cars"])


@router.post(
    "/",
    response_model=shemas.CarResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_car(payload: shemas.CarCreat, db: SessionDep):
    try:
        return car_services.create_car(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Car VIN already exists",
        )


@router.get("/", response_model=list[shemas.CarResponse])
# Отримання списку автомобілів із параметрами фільтрації
def read_cars(
    db: SessionDep,
    brand_model: str | None = None,
    fuel: str | None = None,
    min_year: int | None = None,
    page: int = 1,
    limit: int = 10,
):
    return car_services.get_cars(db, brand_model, fuel, min_year, page, limit)


@router.get("/{car_id}", response_model=list[shemas.CarResponse])
def read_car(car_id: int, db: SessionDep):
    car = car_services.get_car(db, car_id)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_FOUND, detail="Car not fount")
    return car


@router.patch("/{car_id}", response_model=shemas.CarResponse)
def update_car(car_id: int, payload: shemas.CarUpdate, db: SessionDep):
    car = car_services.get_car(db, car_id)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_FOUND, detail="Car not fount")
    try:
        return car_services.update_car(db, car, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Car not updated"
        )


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, db: SessionDep):
    car = car_services.get_car(db, car_id)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_FOUND, detail="Car not fount")
    car_services.delete_car(db, car)
