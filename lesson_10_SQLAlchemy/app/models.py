from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, ConfigDict


class Base(DeclarativeBase):
    pass


class Film(Base):
    __tablename__ = "film"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    year: Mapped[int | None]
    genre: Mapped[str] = mapped_column(String(100))
    producer: Mapped[str | None]
    duration: Mapped[str | None] = mapped_column(String(100))
    actors: Mapped[str | None] = mapped_column(String(100))


model_config = ConfigDict(from_attributes=True)
