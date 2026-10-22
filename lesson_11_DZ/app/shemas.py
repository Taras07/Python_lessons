from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CarBase(BaseModel):
    brand_model: str = Field(min_length=2, max_length=100)
    manufacturer: str = Field(min_length=2, max_length=100)
    vin: str = Field(min_length=17, max_length=17)
    body_type: str = Field(min_length=5, max_length=50)
    engine_volume: float | None = Field(default=None, gt=0)
    fuel: str | None = Field(default=None, min_length=5, max_length=50)
    price: float = Field(gt=0)
    rating: float | None = Field(default=None, gt=0)
    is_available: bool
    description: str | None = Field(default=None, max_length=500)
    year: int
    created_at: datetime
    options: list[str] = Field(default_factory=list)


class CarCreat(CarBase):
    pass


class CarUpdate(BaseModel):
    brand_model: str | None = Field(default=None, min_length=2, max_length=100)
    manufacturer: str | None = Field(default=None, min_length=2, max_length=100)
    body_type: str | None = Field(default=None, min_length=5, max_length=50)
    engine_volume: float | None = Field(default=None, gt=0)
    fuel: str | None = Field(default=None, min_length=5, max_length=50)
    price: float | None = Field(default=None, gt=0)
    rating: float | None = Field(default=None, gt=0)
    is_available: bool | None = None
    description: str | None = Field(default=None, max_length=500)
    year: int | None = None
    options: list[str] | None = None


class CarResponse(BaseModel):
    id: int
    brand_model: str
    manufacturer: str
    vin: str
    body_type: str
    engine_volume: float | None
    fuel: str | None
    price: float
    rating: float | None
    is_available: bool
    description: str | None
    year: int
    created_at: datetime
    options: list[str]

    model_config = ConfigDict(from_attributes=True)
