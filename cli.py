# cli.py
import requests

API_BASE = "http://127.0.0.1:5000"


def _print_table(rows, headers):
    if not rows:
        print("No items found")
        return

    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))

    def fmt_row(values):
        return " | ".join(str(value).ljust(widths[index]) for index, value in enumerate(values))

    print(fmt_row(headers))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(fmt_row(row))


def list_inventory():
    resp = requests.get(f"{API_BASE}/inventory")
    items = resp.json()
    rows = [[item.get("id", ""), item.get("product_name", ""), item.get("stock", ""), item.get("price", "")] for item in items]
    _print_table(rows, ["ID", "Product", "Stock", "Price"])


def view_item():
    item_id = int(input("Enter item ID: "))
    resp = requests.get(f"{API_BASE}/inventory/{item_id}")
    if resp.status_code != 200:
        print(resp.status_code, resp.json())
        return
    item = resp.json()
    rows = [[item.get("id", ""), item.get("product_name", ""), item.get("stock", ""), item.get("price", "")]]
    _print_table(rows, ["ID", "Product", "Stock", "Price"])

def add_item():
    name = input("Product name: ")
    barcode = input("Barcode (optional): ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    data = {
        "product_name": name,
        "barcode": barcode or None,
        "price": price,
        "stock": stock,
    }
    resp = requests.post(f"{API_BASE}/inventory", json=data)
    print(resp.status_code, resp.json())

def update_item():
    item_id = int(input("Item ID to update: "))
    field = input("Field to update (price/stock): ")
    value = input("New value: ")
    if field == "price":
        value = float(value)
    elif field == "stock":
        value = int(value)
    resp = requests.patch(f"{API_BASE}/inventory/{item_id}", json={field: value})
    print(resp.status_code, resp.json())

def delete_item():
    item_id = int(input("Item ID to delete: "))
    resp = requests.delete(f"{API_BASE}/inventory/{item_id}")
    print(resp.status_code)

def import_from_api():
    choice = input("Search by (b)arcode or (n)ame? ")
    if choice == "b":
        barcode = input("Barcode: ")
        resp = requests.post(f"{API_BASE}/inventory/import/barcode/{barcode}")
    else:
        name = input("Product name: ")
        resp = requests.post(f"{API_BASE}/inventory/import/name/{name}")
    print(resp.status_code, resp.json())

def main():
    while True:
        print("""
1. List inventory
2. View item
3. Add item
4. Update item
5. Delete item
6. Import from external API
0. Exit
""")
        choice = input("Choose option: ")
        if choice == "1":
            list_inventory()
        elif choice == "2":
            view_item()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            import_from_api()
        elif choice == "0":
            break

if __name__ == "__main__":
    main()
