from sqlalchemy.orm import Session

from ..shemas import CarCreat, CarUpdate
from ..models import Car
from sqlalchemy import select


# •	Створення автомобіля
def create_car(session: Session, payload: CarCreat) -> Car:
    car = Car(**payload.model_dump())
    session.add(car)
    session.commit()
    session.refresh(car)
    return car


# •	Перелік автомобілів з фільтрами за маркою, типом пального, мінімальним роком випуску та пагінацією
def get_cars(
    session: Session,
    brand_model: str | None = None,
    fuel: str | None = None,
    min_year: int | None = None,
    page: int = 1,
    limit: int = 10,
):
    stmt = select(Car)
    if brand_model is not None:
        stmt = stmt.where(Car.brand_model == brand_model)

    if min_year is not None:
        stmt = stmt.where(Car.year >= min_year)

    if fuel is not None:
        stmt = stmt.where(Car.fuel == fuel)
    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)
    return list(session.scalars(stmt).all())


# •	Перегляд одного автомобіля за ID
def get_car(session: Session, car_id: int) -> Car | None:
    return session.get(Car, car_id)


# •	Часткове оновлення автомобіля
def update_car(session: Session, car: Car, payload: CarUpdate) -> Car:
    changes_dict = payload.model_dump(exclude_unset=True)

    for field, value in changes_dict.items():
        setattr(car, field, value)

    session.commit()
    session.refresh(car)

    return car


# •	Видалення автомобіля
def delete_car(session: Session, car: Car) -> None:
    session.delete(car)
    session.commit()
