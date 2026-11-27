from fastapi.testclient import TestClient

from app.main import app
from app.products import products

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "catalog"}


def test_get_all_products():
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == products
    assert len(response.json()) == 4


def test_get_existing_product():
    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Wireless Headphones"


def test_get_non_existing_product():
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_get_product_has_required_fields():
    response = client.get("/products/1")

    product = response.json()

    assert "id" in product
    assert "name" in product
    assert "description" in product
    assert "price" in product
    assert "image" in product
    assert "category" in product
    assert "stock" in product
