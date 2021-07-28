# from sunflower.main import get_reviews_by_product_url, test, save_html
# from sunflower import settings
from pprint import pprint
from sunflower.marketplaces.mglu.core import MagazineLuizaSunflower
from sunflower.db import Database
from sunflower.db.models import models_list

if __name__ == "__main__":
    mglu = MagazineLuizaSunflower()
    categories = mglu.get_categories()
    # db = Database()
    # db.create_tables(models_list)
