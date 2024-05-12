import yaml
import os

from src.gmaps import Gmaps

with open("params.yaml", "r") as file:
    config = yaml.safe_load(file)

Gmaps.places(
    queries=config["queries"],
    bucket_name=os.getenv("GCS_BUCKET_NAME"),
    blob_name=os.getenv("GCS_BLOB_NAME"),
    max=config["max"],
    scrape_reviews=config["scrape_reviews"],
    reviews_max=config["reviews_max"],
    lang=config["lang"],
)
