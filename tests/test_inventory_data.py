import pytest

import inventory_data as db


@pytest.fixture(autouse=True)
def reset_store():
    db.reset()
    yield
    db.reset()


def test_add_item_creates_item_with_id():
    item = db.add_item({"name": "Almond Milk", "price": 3.5, "quantity": 10})
    assert item["id"] == 1
    assert item["name"] == "Almond Milk"
    assert item["price"] == 3.5
    assert item["quantity"] == 10


def test_add_item_requires_name():
    with pytest.raises(ValueError):
        db.add_item({"price": 1.0})


def test_get_all_items_returns_all_added_items():
    db.add_item({"name": "Item A"})
    db.add_item({"name": "Item B"})
    items = db.get_all_items()
    assert len(items) == 2
    assert {i["name"] for i in items} == {"Item A", "Item B"}


def test_get_item_by_id_found_and_missing():
    item = db.add_item({"name": "Item A"})
    assert db.get_item_by_id(item["id"])["name"] == "Item A"
    assert db.get_item_by_id(9999) is None


def test_update_item_changes_only_given_fields():
    item = db.add_item({"name": "Item A", "price": 1.0, "quantity": 5})
    updated = db.update_item(item["id"], {"price": 2.5})
    assert updated["price"] == 2.5
    assert updated["quantity"] == 5
    assert updated["name"] == "Item A"


def test_update_item_returns_none_for_missing_item():
    assert db.update_item(9999, {"price": 1.0}) is None


def test_delete_item_removes_item():
    item = db.add_item({"name": "Item A"})
    assert db.delete_item(item["id"]) is True
    assert db.get_item_by_id(item["id"]) is None


def test_delete_item_returns_false_for_missing_item():
    assert db.delete_item(9999) is False
