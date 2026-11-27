from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_products():
    products = [{"id": 1, "name": "Headphones", "price": 59.99}]

    mock_response = MagicMock()
    mock_response.json.return_value = products
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    with patch("app.main.httpx.AsyncClient") as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value = mock_client

        response = client.get("/api/products")

    assert response.status_code == 200
    assert response.json() == products


def test_catalog_unavailable():
    with patch(
        "app.main.httpx.AsyncClient", side_effect=Exception("Catalog unavailable")
    ):
        response = client.get("/api/products")

    assert response.status_code == 500
