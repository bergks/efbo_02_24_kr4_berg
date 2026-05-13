from fastapi import FastAPI
from exception import CustomExceptionA, CustomExceptionB
from handlers import custom_a_handler, custom_b_handler

app = FastAPI(title="Custom Exceptions Demo")

app.add_exception_handler(CustomExceptionA, custom_a_handler)
app.add_exception_handler(CustomExceptionB, custom_b_handler)


@app.get("/")
async def root():
    return {"message": "Custom Exceptions API"}


@app.get("/products/{product_id}/buy")
async def buy_product(product_id: int, quantity: int = 1):
    stock = 5

    if quantity > stock:
        raise CustomExceptionA(
            message=f"Недостаточно товара на складе. "
                    f"Запрошено: {quantity}, в наличии: {stock}"
        )

    return {
        "message": f"Товар {product_id} куплен в количестве {quantity}",
        "remaining_stock": stock - quantity
    }


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    products = {1: "Ноутбук", 2: "Мышь", 3: "Клавиатура"}

    if product_id not in products:
        raise CustomExceptionB(resource_name=f"Товар с id={product_id}")

    return {"id": product_id, "name": products[product_id]}