from app import app


def test_get_inventory():
    client = app.test_client()
    resp = client.get("/inventory")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_create_inventory_item():
    client = app.test_client()
    resp = client.post("/inventory", json={
        "product_name": "Test Product",
        "stock": 5,
        "price": 1.99
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["product_name"] == "Test Product"
