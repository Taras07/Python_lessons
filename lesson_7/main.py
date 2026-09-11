from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float


app = FastAPI()


machinery_clasic = [
    {"item_name": "Nokai", "price": 3200},
    {"item_name": "Samsung", "price": 5400},
    {"item_name": "iPhone", "price": 10340},
    {"item_name": "Motorola", "price": 6200},
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/")
def machinery_list():
    return machinery_clasic


@app.post("/items")
def machinery_post(item: Item):
    machinery_clasic.append({"item_name": item.name, "price": item.price})
    return {"message": "Техніка створена", "item": item}


@app.delete("/items/{machineri_id}")
async def machineri_delete(machineri_id: str, needy: str):
    return {"machineri_id": machineri_id, "needy": needy}


@app.put("/items/{machineri_id}")
def update_item(machineri_id: int, machineri: Item):
    return {"machineri_id": machineri_id, "machineri": machineri}


@app.get("/items/{machineri_id}")
def machineri_by_id(machineri_id: int, currency: str = "GRN"):
    product = machinery_clasic[machineri_id].copy()
    if currency:
        if currency == "DOLLAR":
            product["price"] /= 45
        elif currency == "EURO":
            product["price"] /= 51
    return product
