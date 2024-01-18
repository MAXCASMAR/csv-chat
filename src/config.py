import os


FILENAME = "listings.csv"
TABLE_NAME = "listings"
REPLICATE_MODEL_ID = "mistralai/mixtral-8x7b-instruct-v0.1:cf18decbf51c27fed6bbdc3492312c1c903222a56e3fe9ca02d6cbe5198afc10"
 
ROOT_PATH = os.getcwd()
CSV_PATH = os.path.join(ROOT_PATH, FILENAME)

SCHEMA = {
    "id": "TEXT",
    "listing_type": "TEXT",
    "property_type": "TEXT",
    "last_price": "NUMERIC",
    "num_bedrooms": "INTEGER",
    "num_bathrooms": "INTEGER",
    "has_pool": "BOOLEAN",
    "has_terrace": "BOOLEAN",
    "surface_total": "INTEGER"
}
