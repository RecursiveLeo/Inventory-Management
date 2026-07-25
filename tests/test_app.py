from unittest.mock import patch

import pytest

import inventory_data as db
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    db.reset()
    with app.test_client() as client:
        yield client
    db.reset()


# ---------------------------------------------------------------------------
# CRUD endpoint tests
# ---------------------------------------------------------------------------


def test_get_inventory_empty(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_and_get_item(client):
    response = client.post("/inventory", json={"name": "Almond Milk", "price": 3.5})
    assert response.status_code == 201
    item_id = response.get_json()["id"]

    response = client.get(f"/inventory/{item_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Almond Milk"


def test_create_item_missing_name_returns_400(client):
    response = client.post("/inventory", json={"price": 3.5})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_missing_item_returns_404(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


def test_patch_updates_item(client):
    created = client.post("/inventory", json={"name": "Item A", "quantity": 5})
    item_id = created.get_json()["id"]

    response = client.patch(f"/inventory/{item_id}", json={"quantity": 20})
    assert response.status_code == 200
    assert response.get_json()["quantity"] == 20


def test_patch_missing_item_returns_404(client):
    response = client.patch("/inventory/999", json={"quantity": 1})
    assert response.status_code == 404


def test_delete_item(client):
    created = client.post("/inventory", json={"name": "Item A"})
    item_id = created.get_json()["id"]

    response = client.delete(f"/inventory/{item_id}")
    assert response.status_code == 204

    response = client.get(f"/inventory/{item_id}")
    assert response.status_code == 404


def test_delete_missing_item_returns_404(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# External API endpoint tests (mocked)
# ---------------------------------------------------------------------------


@patch("app.fetch_product_by_barcode")
def test_lookup_product_by_barcode_found(mock_fetch, client):
    mock_fetch.return_value = {
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "1234567890",
        "category": "Beverages",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "source": "openfoodfacts",
    }

    response = client.get("/products/barcode/1234567890")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Organic Almond Milk"
    mock_fetch.assert_called_once_with("1234567890")


@patch("app.fetch_product_by_barcode")
def test_lookup_product_by_barcode_not_found(mock_fetch, client):
    mock_fetch.return_value = None
    response = client.get("/products/barcode/0000000000")
    assert response.status_code == 404


@patch("app.fetch_product_by_name")
def test_search_products_by_name(mock_fetch, client):
    mock_fetch.return_value = [
        {"name": "Almond Milk", "brand": "Silk", "barcode": "111", "source": "openfoodfacts"}
    ]
    response = client.get("/products/search", query_string={"name": "almond milk"})
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_search_products_missing_query_param(client):
    response = client.get("/products/search")
    assert response.status_code == 400


@patch("app.fetch_product_by_barcode")
def test_import_inventory_item_by_barcode(mock_fetch, client):
    mock_fetch.return_value = {
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "1234567890",
        "category": "Beverages",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "source": "openfoodfacts",
    }

    response = client.post("/inventory/import/barcode/1234567890", json={"price": 4.99})
    assert response.status_code == 201
    body = response.get_json()
    assert body["name"] == "Organic Almond Milk"
    assert body["price"] == 4.99
    assert body["source"] == "openfoodfacts"

    # It should actually land in the inventory store.
    response = client.get("/inventory")
    assert len(response.get_json()) == 1
