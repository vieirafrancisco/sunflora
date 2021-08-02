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
    categories = mglu.get_categories()
    logging.debug(f"Loaded {len(categories)} categories.")

@click.command()
def load_products():
    """Load products from categories"""
    products = mglu.get_products()
    logging.debug(f"Loaded {len(products)} products.")

@click.command()
@click.option("--product", "-p", type=int, required=True)
def load_reviews(product):
    reviews = mglu.get_product_reviews(product)
    logging.debug(f"Loaded {len(reviews)} reviews.")

api.add_command(load_categories)
api.add_command(load_products)
api.add_command(load_reviews)
