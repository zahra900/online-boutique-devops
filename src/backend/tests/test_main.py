from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_products():
    products = [{"id": 1, "name": "Headphones", "price": 59.99}]

    mock_response = AsyncMock()
    mock_response.json.return_value = products
    mock_response.raise_for_status.return_value = None

    with patch("app.main.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )

        response = client.get("/api/products")

    assert response.status_code == 200
    assert response.json() == products


def test_catalog_unavailable():
    with patch(
        "app.main.httpx.AsyncClient",
        side_effect=Exception("Catalog unavailable")
    ):
        response = client.get("/api/products")

    assert response.status_code == 500