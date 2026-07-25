# Inventory Management System

A Flask REST API for a retail company's admin portal, backed by an in-memory
inventory store, with real-time product lookups from the
[OpenFoodFacts](https://world.openfoodfacts.org/) API and a CLI front end.

## Features

- Full CRUD REST API for inventory items (`GET`, `POST`, `PATCH`, `DELETE`)
- Product lookup by barcode or name against the OpenFoodFacts API
- One-call "import" endpoint that fetches a product from OpenFoodFacts and
  adds it straight to inventory
- CLI tool that drives the API: view inventory, add/update/delete items,
  and search OpenFoodFacts
- Unit tests (pytest + unittest.mock) for the data layer, the Flask routes,
  the external API client, and the CLI

## Project Structure

```
Inventory-Management/
├── app.py                # Flask app & routes
├── inventory_data.py      # In-memory "database" + CRUD helpers
├── external_api.py        # OpenFoodFacts integration
├── requirements.txt
├── pytest.ini
├── cli/
│   └── cli.py             # CLI front end
└── tests/
    ├── test_app.py
    ├── test_inventory_data.py
    ├── test_external_api.py
    └── test_cli.py
```

## Installation

```bash
git clone <this-repo-url>
cd Inventory-Management
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the API

```bash
python app.py
```

The server runs on `http://localhost:5555` with Flask debug mode on.

## API Endpoints

### Inventory CRUD

| Method | Route | Description |
|---|---|---|
| GET | `/inventory` | List all inventory items |
| GET | `/inventory/<id>` | Get a single item |
| POST | `/inventory` | Create an item (`name` required; `brand`, `barcode`, `category`, `price`, `quantity`, `ingredients_text` optional) |
| PATCH | `/inventory/<id>` | Update one or more fields on an item |
| DELETE | `/inventory/<id>` | Delete an item |

### External API helpers

| Method | Route | Description |
|---|---|---|
| GET | `/products/barcode/<barcode>` | Look up a product on OpenFoodFacts by barcode |
| GET | `/products/search?name=<query>` | Search OpenFoodFacts by product name |
| POST | `/inventory/import/barcode/<barcode>` | Fetch a product by barcode and add it directly to inventory (optional JSON body to override fields like `price`) |

### Example requests

```bash
curl -X POST http://localhost:5555/inventory \
  -H "Content-Type: application/json" \
  -d '{"name": "Almond Milk", "brand": "Silk", "price": 3.99, "quantity": 20}'

curl http://localhost:5555/products/barcode/3017620422003

curl -X POST http://localhost:5555/inventory/import/barcode/3017620422003 \
  -H "Content-Type: application/json" \
  -d '{"price": 4.49, "quantity": 15}'
```

## Using the CLI

With the Flask server running in one terminal, run the CLI in another:

```bash
python cli/cli.py
```

You'll get a menu:

```
Inventory Management CLI
1. View inventory
2. Add new item
3. Update item price/stock
4. Delete item
5. Find item on external API
6. Quit
```

- **View inventory** — prints a table of all items currently in stock.
- **Add new item** — prompts for name, brand, price, and quantity, then POSTs to `/inventory`.
- **Update item price/stock** — prompts for an item id, then a new price and/or quantity (leave blank to keep current value), and PATCHes `/inventory/<id>`.
- **Delete item** — prompts for an item id and DELETEs it.
- **Find item on external API** — search OpenFoodFacts by barcode or name; a barcode match can be added straight to inventory.

## Running Tests

```bash
pytest
```

Tests cover:
- `inventory_data.py` — add/get/update/delete logic on the in-memory store
- `app.py` — every CRUD route plus the external-API routes (with `external_api` calls mocked)
- `external_api.py` — barcode/name lookups, found/not-found cases, and network-failure handling (with `requests` mocked)
- `cli/cli.py` — each CLI action, with HTTP calls and `input()` mocked

## Notes

- Inventory data is stored in memory and resets whenever the Flask process restarts — there's no database in this version, as specified in the lab (a simulated array-backed store).
- The OpenFoodFacts endpoints require outbound internet access to `world.openfoodfacts.org`.
