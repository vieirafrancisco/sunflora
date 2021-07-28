import click

from sunflower.settings import logging
from sunflower.marketplaces.mglu.core import MagazineLuizaSunflower

mglu = MagazineLuizaSunflower()

@click.group()
def api():
    pass

@click.command()
def load_categories():
    categories = mglu.get_categories()
    logging.debug(f"Loaded {len(categories)} categories.")

api.add_command(load_categories)
