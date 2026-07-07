import requests

BASE_URL = "https://world.openfoodfacts.org"


def fetch_product_by_barcode(barcode: str):
    url = f"{BASE_URL}/api/v0/product/{barcode}.json"
    resp = requests.get(url, timeout=5)
    if resp.status_code != 200:
        return None
    data = resp.json()
    if data.get("status") != 1:
        return None
    product = data.get("product", {})
    return {
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
    }


def fetch_product_by_name(name: str):
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
    }
    resp = requests.get(url, params=params, timeout=5)
    if resp.status_code != 200:
        return None
    data = resp.json()
    products = data.get("products", [])
    if not products:
        return None
    product = products[0]
    return {
        "barcode": product.get("code"),
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
    }
