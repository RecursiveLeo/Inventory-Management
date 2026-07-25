"""Helpers for talking to the OpenFoodFacts public API."""

import requests

BASE_URL = "https://world.openfoodfacts.org"
TIMEOUT = 10


class ExternalAPIError(Exception):
    """Raised when the OpenFoodFacts API can't be reached or returns bad data."""


def fetch_product_by_barcode(barcode):
    """Look up a single product by its barcode.

    Returns a normalized dict of product fields, or None if no product
    was found for that barcode.
    Raises ExternalAPIError on network/API failures.
    """
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExternalAPIError(f"Failed to reach OpenFoodFacts: {exc}") from exc

    data = response.json()
    if data.get("status") != 1:
        return None

    return _normalize_product(data["product"], barcode=barcode)


def fetch_product_by_name(name, limit=5):
    """Search for products by name.

    Returns a list of normalized product dicts (possibly empty).
    Raises ExternalAPIError on network/API failures.
    """
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": limit,
    }
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExternalAPIError(f"Failed to reach OpenFoodFacts: {exc}") from exc

    data = response.json()
    products = data.get("products", [])
    return [_normalize_product(p) for p in products[:limit]]


def _normalize_product(product, barcode=None):
    return {
        "name": product.get("product_name") or "Unknown product",
        "brand": product.get("brands"),
        "barcode": barcode or product.get("code"),
        "category": product.get("categories"),
        "ingredients_text": product.get("ingredients_text"),
        "source": "openfoodfacts",
    }
