import os

import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Mini Shop Backend")

CATALOG_URL = os.getenv("CATALOG_URL", "http://localhost:8001")


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "backend"}


@app.get("/api/products")
async def get_products():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(CATALOG_URL)
            response.raise_for_status()
            return response.json()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail="Catalog service unavailable",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Catalog service unavailable",
        )
