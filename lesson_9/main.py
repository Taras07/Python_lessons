from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

coffee = [
    {"id": 1, "name": "Еспресо", "price": 90},
    {"id": 2, "name": "Допіо", "price": 110},
    {"id": 3, "name": "Рістрето", "price": 130},
    {"id": 4, "name": "Лунго", "price": 120},
    {"id": 5, "name": "Американо", "price": 80},
]


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/products")
def products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={"coffee": coffee},
    )


@app.get("/contacts")
def contacts(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contacts.html",
    )


@app.get("/products/new")
def new_products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="form.html",
    )


@app.get("/products/{product_id}/edit")
def edit_product(product_id: int, request: Request):
    product = next(item for item in coffee if item["id"] == product_id)
    return templates.TemplateResponse(
        request=request, name="form.html", context={"product": product}
    )


@app.post("/products/{product_id}")
def update_product(
    product_id: int,
    name: Annotated[str, Form()],
    price: Annotated[int, Form()],
):
    for item in coffee:
        if item["id"] == product_id:
            item["name"] = name
            item["price"] = price
            break

    return RedirectResponse(
        url="/products",
        status_code=303,
    )


@app.post("/products/{product_id}/delete")
def delete_product(product_id: int):
    for item in coffee:
        if item["id"] == product_id:
            coffee.remove(item)
            break

    return RedirectResponse(
        url="/products",
        status_code=303,
    )


# Що тут відбувається:

# product_id отримує ID кави, яку видаляємо.
# for item in coffee: перебирає всі кави.
# if item["id"] == product_id: шукає потрібну.
# coffee.remove(item) видаляє її зі списку.
# break зупиняє цикл.
# RedirectResponse повертає нас до списку кави.
# Після цього перевір «Видалити». ☕🗑️

# =======================


@app.post("/products")
def creat_product(
    name: Annotated[str, Form()],
    price: Annotated[int, Form()],
):
    new_id = max(item["id"] for item in coffee) + 1
    coffee.append(
        {
            "id": new_id,
            "name": name,
            "price": price,
        }
    )

    return RedirectResponse(
        url="/products",
        status_code=303,
    )


# ===========================================================
# @app.get("/")
# def read_root(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="index.html",
#         context={"user": "Ivan", "age": 25, "notes": notes},
#     )


# @app.post("/add")
# def add_note(
#     title: Annotated[str, Form(min_length=3)],
#     importance: Annotated[int, Form(gt=0)],
# ):
#     notes.append({"id": len(notes) + 1, "title": title, "importance": importance})
#     return RedirectResponse("/", status_code=303)


# @app.post("/delete/{id}")
# def delete_note(id: int):
#     global notes
#     notes = [note for note in notes if note.get("id") != id]
#     return RedirectResponse("/", status_code=303)


# @app.post("/edit/{id}")
# def edit_note(id: int, request: Request):
#     for note in notes:
#         if note.get("id") == id:
#             return templates.TemplateResponse(
#                 request=request,
#                 name="index.html",
#                 context={"user": "Ivan", "age": 25, "notes": notes, "edit_note": note},
#             )
#     return RedirectResponse("/", status_code=303)


# @app.post("/save/{id}")
# def save_note(
#     id: int,
#     title: Annotated[str, Form(min_length=3)],
#     importance: Annotated[int, Form(gt=0)],
# ):
#     for note in notes:
#         if note.get("id") == id:
#             note["title"] = title
#             note["importance"] = importance
#     return RedirectResponse("/", status_code=303)
