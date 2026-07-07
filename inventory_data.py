inventory = [
    {
        "id": 1,
        "barcode": "1234567890123",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "stock": 10,
        "price": 4.99
    },
    {
        "id": 2,
        "barcode": "9876543210987",
        "product_name": "Whole Grain Bread",
        "brands": "Nature's Own",
        "ingredients_text": "Whole wheat flour, water, yeast, salt",
        "stock": 25,
        "price": 2.49
    }
]


def get_all_items():
    return inventory


def get_item_by_id(item_id: int):
    return next((item for item in inventory if item["id"] == item_id), None)


def add_item(item: dict):
    new_id = max([i["id"] for i in inventory], default=0) + 1
    item["id"] = new_id
    inventory.append(item)
    return item


def update_item(item_id: int, updates: dict):
    item = get_item_by_id(item_id)
    if not item:
        return None
    item.update(updates)
    return item


def delete_item(item_id: int):
    global inventory
    before = len(inventory)
    inventory = [i for i in inventory if i["id"] != item_id]
    return len(inventory) < before
