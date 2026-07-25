from unittest.mock import patch, MagicMock

from cli import cli


@patch("cli.cli._get")
def test_view_inventory_prints_items(mock_get, capsys):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": 1, "name": "Almond Milk", "brand": "Silk", "price": 3.5, "quantity": 10}
    ]
    mock_get.return_value = mock_response

    cli.view_inventory()

    captured = capsys.readouterr()
    assert "Almond Milk" in captured.out


@patch("cli.cli._get")
def test_view_inventory_handles_empty(mock_get, capsys):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    cli.view_inventory()

    captured = capsys.readouterr()
    assert "Inventory is empty." in captured.out


@patch("cli.cli._post")
@patch("builtins.input", side_effect=["Almond Milk", "Silk", "3.50", "10"])
def test_add_item_posts_payload(mock_input, mock_post, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1}
    mock_post.return_value = mock_response

    cli.add_item()

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "/inventory"
    assert kwargs["json"]["name"] == "Almond Milk"
    captured = capsys.readouterr()
    assert "Added item with id 1." in captured.out


@patch("cli.cli._patch")
@patch("builtins.input", side_effect=["1", "", "25"])
def test_update_item_patches_only_given_fields(mock_input, mock_patch, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "quantity": 25}
    mock_patch.return_value = mock_response

    cli.update_item()

    args, kwargs = mock_patch.call_args
    assert args[0] == "/inventory/1"
    assert kwargs["json"] == {"quantity": 25}


@patch("cli.cli._delete")
@patch("builtins.input", side_effect=["1"])
def test_delete_item_success(mock_input, mock_delete, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response

    cli.delete_item()

    mock_delete.assert_called_once_with("/inventory/1")
    captured = capsys.readouterr()
    assert "Item deleted." in captured.out


@patch("cli.cli._get")
def test_find_on_external_api_by_barcode_declines_add(mock_get, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "Almond Milk", "brand": "Silk"}
    mock_get.return_value = mock_response

    with patch("builtins.input", side_effect=["barcode", "1234567890", "n"]):
        cli.find_on_external_api()

    captured = capsys.readouterr()
    assert "Found: Almond Milk" in captured.out
