import yaml

from src.gmaps import Gmaps

with open("params.yaml", "r") as file:
    config = yaml.safe_load(file)

Gmaps.places(
    queries=config["queries"],
    max=config["max"],
    scrape_reviews=config["scrape_reviews"],
    reviews_max=config["reviews_max"],
    lang=config["lang"],
)
