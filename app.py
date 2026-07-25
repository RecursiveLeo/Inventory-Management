from flask import Flask, request, jsonify, make_response

import inventory_data as db
from external_api import fetch_product_by_barcode, fetch_product_by_name, ExternalAPIError

app = Flask(__name__)


def error_response(message, status=400):
    return make_response(jsonify({"error": message}), status)


# ---------------------------------------------------------------------------
# CRUD routes
# ---------------------------------------------------------------------------


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(db.get_all_items()), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = db.get_item_by_id(item_id)
    if item is None:
        return error_response("Item not found", 404)
    return jsonify(item), 200


@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    data = request.get_json(silent=True) or {}
    try:
        item = db.add_item(data)
    except ValueError as exc:
        return error_response(str(exc), 400)
    return jsonify(item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json(silent=True) or {}
    item = db.update_item(item_id, data)
    if item is None:
        return error_response("Item not found", 404)
    return jsonify(item), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    deleted = db.delete_item(item_id)
    if not deleted:
        return error_response("Item not found", 404)
    return "", 204


# ---------------------------------------------------------------------------
# External API helper routes
# ---------------------------------------------------------------------------


@app.route("/products/barcode/<barcode>", methods=["GET"])
def lookup_product_by_barcode(barcode):
    try:
        product = fetch_product_by_barcode(barcode)
    except ExternalAPIError as exc:
        return error_response(str(exc), 502)

    if product is None:
        return error_response("No product found for that barcode", 404)
    return jsonify(product), 200


@app.route("/products/search", methods=["GET"])
def search_products_by_name():
    name = request.args.get("name")
    if not name:
        return error_response("Query parameter 'name' is required", 400)

    try:
        products = fetch_product_by_name(name)
    except ExternalAPIError as exc:
        return error_response(str(exc), 502)

    return jsonify(products), 200


@app.route("/inventory/import/barcode/<barcode>", methods=["POST"])
def import_inventory_item_by_barcode(barcode):
    """Fetch a product from OpenFoodFacts and add it straight to inventory."""
    try:
        product = fetch_product_by_barcode(barcode)
    except ExternalAPIError as exc:
        return error_response(str(exc), 502)

    if product is None:
        return error_response("No product found for that barcode", 404)

    overrides = request.get_json(silent=True) or {}
    product.update({k: v for k, v in overrides.items() if v is not None})

    item = db.add_item(product)
    return jsonify(item), 201


if __name__ == "__main__":
    app.run(debug=True, port=5555)
