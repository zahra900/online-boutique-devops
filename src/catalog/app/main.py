from fastapi import FastAPI, HTTPException
from app.products import products

app = FastAPI(title="Mini Shop Catalog Service")


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "catalog"
    }


@app.get("/products")
async def get_products():
    return products


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product