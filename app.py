from flask import Flask, jsonify, request
from inventory_data import (
    get_all_items, get_item_by_id,
    add_item, update_item, delete_item
)
from external_api import fetch_product_by_barcode, fetch_product_by_name

app = Flask(__name__)

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(get_all_items()), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = get_item_by_id(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    data = request.get_json()
    if not data or "product_name" not in data:
        return jsonify({"error": "Invalid data"}), 400
    item = add_item({
        "barcode": data.get("barcode"),
        "product_name": data["product_name"],
        "brands": data.get("brands"),
        "ingredients_text": data.get("ingredients_text"),
        "stock": data.get("stock", 0),
        "price": data.get("price", 0.0),
    })
    return jsonify(item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def patch_inventory_item(item_id):
    data = request.get_json() or {}
    item = update_item(item_id, data)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item_route(item_id):
    deleted = delete_item(item_id)
    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    return "", 204

@app.route("/inventory/import/barcode/<barcode>", methods=["POST"])
def import_by_barcode(barcode):
    product = fetch_product_by_barcode(barcode)
    if not product:
        return jsonify({"error": "Product not found in external API"}), 404
    item = add_item({
        "barcode": barcode,
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
        "stock": 0,
        "price": 0.0,
    })
    return jsonify(item), 201

@app.route("/inventory/import/name/<name>", methods=["POST"])
def import_by_name(name):
    product = fetch_product_by_name(name)
    if not product:
        return jsonify({"error": "Product not found in external API"}), 404
    item = add_item({
        "barcode": product.get("barcode"),
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
        "stock": 0,
        "price": 0.0,
    })
    return jsonify(item), 201

if __name__ == "__main__":
    app.run(debug=True)
