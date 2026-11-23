from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI(title="Mini Shop Backend")

CATALOG_URL = os.getenv(
    "CATALOG_URL",
    "http://localhost:8001"
)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "backend"}


@app.get("/api/products")
async def get_products():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{CATALOG_URL}/products"
            )

            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Catalog service unavailable"
        ) from exc