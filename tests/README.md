# Inventory Management System – Flask REST API

## Installation

- Clone repo
- Create virtualenv
- `pip install -r requirements.txt`
- Run API: `python app.py`
- Run CLI: `python cli.py`

## API Endpoints

- `GET /inventory`
- `GET /inventory/<id>`
- `POST /inventory`
- `PATCH /inventory/<id>`
- `DELETE /inventory/<id>`
- `POST /inventory/import/barcode/<barcode>`
- `POST /inventory/import/name/<name>`

## CLI Usage

Examples:
- List inventory
- Add item
- Update stock/price
- Delete item
- Import from external API
