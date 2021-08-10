import click

from sunflower.settings import logging
from sunflower.marketplaces.mglu.core import MagazineLuizaSunflower

mglu = MagazineLuizaSunflower()

@click.group()
def api():
    pass

@click.command()
def load_categories():
    """Load categories from mglu marketplace"""
    categories = mglu.load_categories()
    logging.info(f"Loaded {len(categories)} categories.")

@click.command()
def load_products():
    """Load products from categories"""
    products = mglu.load_products()
    logging.info(f"Loaded {len(products)} products.")

@click.command()
@click.option("--product", "-p", type=int, required=True)
def load_reviews(product):
    reviews = mglu.load_product_reviews(product)
    logging.info(f"Loaded {len(reviews)} reviews.")

api.add_command(load_categories)
api.add_command(load_products)
api.add_command(load_reviews)
