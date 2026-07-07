from unittest.mock import patch
from external_api import fetch_product_by_barcode


@patch("external_api.requests.get")
def test_fetch_product_by_barcode(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Mock Milk",
            "brands": "MockBrand",
            "ingredients_text": "Water, mock"
        }
    }
    product = fetch_product_by_barcode("123")
    assert product["product_name"] == "Mock Milk"
