from datetime import datetime

from sqlalchemy import Float, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Car(Base):
    __tablename__ = "cars"

    # •	унікальний номер автомобіля
    id: Mapped[int] = mapped_column(primary_key=True)
    # •	марка та модель автомобіля
    brand_model: Mapped[str] = mapped_column(String(100))
    # •	ім’я виробника або дилера
    manufacturer: Mapped[str] = mapped_column(String(100))
    # •	він-код (VIN), як унікальний паспорт транспортного засобу
    vin: Mapped[str] = mapped_column(String(17), unique=True)
    # •	тип кузова (наприклад, седан, кросовер, хетчбек)
    body_type: Mapped[str] = mapped_column(String(50))
    # •	об'єм двигуна у літрах або потужність в к.с.
    engine_volume: Mapped[float | None] = mapped_column(Float, nullable=True)
    fuel: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # •	вартість автомобіля
    price: Mapped[float] = mapped_column(Float)
    # •	оцінка від експертів чи покупців (може бути відсутня)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    # •	короткий опис комплектації або технічних характеристик
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # •	рік випуску автомобіля
    year: Mapped[int] = mapped_column(Integer)
    # •	коли автомобіль був доданий в систему/базу
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    # •	список додаткових опцій чи міток (наприклад, "кожа", "автопілот"), може бути порожнім.
    options: Mapped[list[str]] = mapped_column(JSON)
