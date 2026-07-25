"""In-memory 'database' for inventory items.

Each item is a dict shaped roughly like:
{
    "id": int,
    "name": str,
    "brand": str,
    "barcode": str | None,
    "category": str | None,
    "price": float,
    "quantity": int,
    "ingredients_text": str | None,
    "source": "manual" | "openfoodfacts",
}
"""

from itertools import count

_id_counter = count(1)
_inventory = []


def _next_id():
    return next(_id_counter)


def reset():
    """Clear the store and restart the id counter (mainly for tests)."""
    global _id_counter
    _inventory.clear()
    _id_counter = count(1)


def get_all_items():
    return list(_inventory)


def get_item_by_id(item_id):
    for item in _inventory:
        if item["id"] == item_id:
            return item
    return None


def add_item(data):
    """Create a new item from a dict of fields and store it.

    Required: name
    Optional: brand, barcode, category, price, quantity, ingredients_text, source
    """
    if not data.get("name"):
        raise ValueError("'name' is required to add an inventory item.")

    item = {
        "id": _next_id(),
        "name": data["name"],
        "brand": data.get("brand"),
        "barcode": data.get("barcode"),
        "category": data.get("category"),
        "price": float(data.get("price", 0) or 0),
        "quantity": int(data.get("quantity", 0) or 0),
        "ingredients_text": data.get("ingredients_text"),
        "source": data.get("source", "manual"),
    }
    _inventory.append(item)
    return item


def update_item(item_id, data):
    """Partially update an existing item. Returns the updated item, or None
    if no item with that id exists."""
    item = get_item_by_id(item_id)
    if item is None:
        return None

    for field in (
        "name",
        "brand",
        "barcode",
        "category",
        "price",
        "quantity",
        "ingredients_text",
        "source",
    ):
        if field in data and data[field] is not None:
            if field == "price":
                item[field] = float(data[field])
            elif field == "quantity":
                item[field] = int(data[field])
            else:
                item[field] = data[field]

    return item


def delete_item(item_id):
    item = get_item_by_id(item_id)
    if item is None:
        return False
    _inventory.remove(item)
    return True
