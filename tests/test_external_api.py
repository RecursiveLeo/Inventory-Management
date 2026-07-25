from unittest.mock import patch, MagicMock

import pytest
import requests

from external_api import fetch_product_by_barcode, fetch_product_by_name, ExternalAPIError


@patch("external_api.requests.get")
def test_fetch_product_by_barcode_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar",
        },
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    product = fetch_product_by_barcode("1234567890")

    assert product["name"] == "Organic Almond Milk"
    assert product["brand"] == "Silk"
    assert product["barcode"] == "1234567890"
    assert product["source"] == "openfoodfacts"


@patch("external_api.requests.get")
def test_fetch_product_by_barcode_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    assert fetch_product_by_barcode("0000000000") is None


@patch("external_api.requests.get")
def test_fetch_product_by_barcode_network_error(mock_get):
    mock_get.side_effect = requests.ConnectionError("no network")

    with pytest.raises(ExternalAPIError):
        fetch_product_by_barcode("1234567890")


@patch("external_api.requests.get")
def test_fetch_product_by_name_returns_list(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "products": [
            {"product_name": "Almond Milk", "brands": "Silk", "code": "111"},
            {"product_name": "Almond Milk Unsweetened", "brands": "Silk", "code": "222"},
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    products = fetch_product_by_name("almond milk", limit=5)

    assert len(products) == 2
    assert products[0]["name"] == "Almond Milk"
    assert products[0]["barcode"] == "111"


@patch("external_api.requests.get")
def test_fetch_product_by_name_respects_limit(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "products": [{"product_name": f"Item {i}", "code": str(i)} for i in range(10)]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    products = fetch_product_by_name("item", limit=3)
    assert len(products) == 3


@patch("external_api.requests.get")
def test_fetch_product_by_name_network_error(mock_get):
    mock_get.side_effect = requests.Timeout("timed out")

    with pytest.raises(ExternalAPIError):
        fetch_product_by_name("almond milk")
