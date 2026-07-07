from unittest.mock import patch
import cli


def mock_input_sequence(inputs):
    """Helper to simulate multiple input() calls."""
    def side_effect(_=None):
        return inputs.pop(0)
    return side_effect


@patch("requests.get")
def test_list_inventory(mock_get):
    mock_get.return_value.json.return_value = [{"id": 1, "product_name": "Test"}]
    mock_get.return_value.status_code = 200

    with patch("builtins.print") as mock_print:
        cli.list_inventory()
        mock_print.assert_called_with([{"id": 1, "product_name": "Test"}])


@patch("requests.get")
def test_view_item(mock_get):
    mock_get.return_value.json.return_value = {"id": 1, "product_name": "Test"}
    mock_get.return_value.status_code = 200

    with patch("builtins.input", side_effect=["1"]), \
         patch("builtins.print") as mock_print:
        cli.view_item()
        mock_print.assert_any_call(200, {"id": 1, "product_name": "Test"})


@patch("requests.post")
def test_add_item(mock_post):
    mock_post.return_value.json.return_value = {"id": 3, "product_name": "New Item"}
    mock_post.return_value.status_code = 201

    inputs = ["New Item", "12345", "9.99", "5"]
    with patch("builtins.input", side_effect=mock_input_sequence(inputs)), \
         patch("builtins.print") as mock_print:
        cli.add_item()
        mock_print.assert_any_call(201, {"id": 3, "product_name": "New Item"})


@patch("requests.patch")
def test_update_item(mock_patch):
    mock_patch.return_value.json.return_value = {"id": 1, "price": 10.99}
    mock_patch.return_value.status_code = 200

    inputs = ["1", "price", "10.99"]
    with patch("builtins.input", side_effect=mock_input_sequence(inputs)), \
         patch("builtins.print") as mock_print:
        cli.update_item()
        mock_print.assert_any_call(200, {"id": 1, "price": 10.99})


@patch("requests.delete")
def test_delete_item(mock_delete):
    mock_delete.return_value.status_code = 204

    with patch("builtins.input", side_effect=["1"]), \
         patch("builtins.print") as mock_print:
        cli.delete_item()
        mock_print.assert_any_call(204)


@patch("requests.post")
def test_import_from_api_barcode(mock_post):
    mock_post.return_value.json.return_value = {"id": 10, "product_name": "Imported"}
    mock_post.return_value.status_code = 201

    inputs = ["b", "123456"]
    with patch("builtins.input", side_effect=mock_input_sequence(inputs)), \
         patch("builtins.print") as mock_print:
        cli.import_from_api()
        mock_print.assert_any_call(201, {"id": 10, "product_name": "Imported"})
