from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


from fastapi import FastAPI


from app.database import engine
from app.models import Base
from app.routers import car



@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Car catalog", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://taras07.github.io",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(car.router)
