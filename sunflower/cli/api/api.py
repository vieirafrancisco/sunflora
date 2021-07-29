import click

from sunflower.settings import logging
from sunflower.marketplaces.mglu.core import MagazineLuizaSunflower

mglu = MagazineLuizaSunflower()

@click.group()
def api():
    pass

@click.command()
@click.option("--save", "-s", type=bool)
@click.option("--cache", "-c", type=bool)
def load_categories(save=False, cache=True):
    """Load categories from mglu marketplace"""
    categories = mglu.get_categories(save=save, cache=cache)
    logging.debug(f"Loaded {len(categories)} categories.")

@click.command()
@click.option("--save", "-s", type=bool)
def load_products(save=False):
    """Load products from categories"""
    products = mglu.get_products(save=save)
    logging.debug(f"Loaded {len(products)} products.")

api.add_command(load_categories)
api.add_command(load_products)
