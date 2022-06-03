from itertools import product
from unicodedata import name
from sanic import Sanic
from sanic import response

app = Sanic("WarehouseApp")

products_db = [
    {"name": "tv", "model": "model1", "quantity": 1},
    {"name": "mobile", "model": "model1", "quantity": 5},
    {"name": "speaker", "model": "model1", "quantity": 3},
]


@app.get("/")
async def get_products(request):
    id_ = request.args.get("id")
    if id_:
        if int(id_) in range(len(products_db)):
            return response.json(products_db[int(id_)])
        else:
            return response.json(
                {
                    "status": "error",
                    "message": f"Product with id {id_} not found. Try with different id!!!",
                }
            )
    return response.json(products_db)


@app.post("/")
async def add_products(request):
    product = request.json
    check = True
    for i in range(len(products_db)):
        if (
            products_db[i]["name"] == product["name"]
            and products_db[i]["model"] == product["model"]
        ):
            check = False
            products_db[i]["quantity"] += product["quantity"]
            product = products_db[i]
            break
    if check:
        products_db.append(product)
    return response.json(product)


# @app.put("/<id_:int>")
# async def update_product(request, id_):
#     product = request.json
#     print(product)
#     if id_ in range(len(products_db)):
#         product[id_] = product
#     else:
#         return response.json({"error": "No product with given id"})
#     return response.json(product)


@app.delete("/<id_:int>")
async def delete_product(request, id_):
    if id_ in range(len(products_db)):
        del products_db[id_]
    else:
        return response.json({"error": "No Product with given id"})
    return response.json({"message": "Deleted Product successfully"})


@app.post("/buy")
async def buy_products(request):
    product = request.json
    check = True
    quantity = 0
    for i in range(len(products_db)):
        if (
            products_db[i]["name"] == product["name"]
            and products_db[i]["model"] == product["model"]
        ):
            check = False
            quantity = products_db[i]["quantity"]
            if product["quantity"] > quantity:
                return response.json(
                    {"message": f"We only have {quantity} of the product"}
                )
            products_db[i]["quantity"] -= product["quantity"]
            quantity -= product["quantity"]
            product = products_db[i]
            break
    if check:
        return response.json({"message": "No Product with the given details found"})
    return response.json(
        {"message": f"Product sold to customer. Remaning quantity : {quantity}"}
    )


app.run(host="0.0.0.0", port=8000)
