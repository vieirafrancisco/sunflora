import os
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from sunflower import Sunflower
from sunflower.utils import save_html, load_html
from sunflower.db.models import Category
from sunflower.db import IntegrityError
from sunflower.settings import logging

from .utils import make_GET_request, regex_categories


class MagazineLuizaSunflower(Sunflower):
    def __init__(self):
        super().__init__(marketplace_url="https://www.magazineluiza.com.br/")

    def get_categories(self, save=False, cache=True):
        categories = list()
        html = make_GET_request(
            self.marketplace_url,
            file_name="mglu_categories.html",
            cache=cache
        )
        for category in regex_categories(html):
            parent = None
            if category["parent"] is not None:
                parent = Category.select().where(
                    (Category.name == category["parent"]["name"]) &
                    (Category.initials == category["parent"]["initials"])
                )
            try:
                c = Category.create(
                    name=category["name"],
                    initials=category["initials"],
                    url=category["url"],
                    parent=parent
                )
            except IntegrityError as e:
                logging.error(e)
                logging.error(f"Category '{category['name']}' with initials '{category['initials']}' already exist!")
            else:
                categories.append(c)
        return categories

    def get_products_by_category(self, category, max_num=100, save=False, start_page=1):
        pass

    def get_random_products(self, save=False):
        pass
    
    def get_product_reviews(self, product):
        pass

    def get_product_reviews_by_url(self, product_url):
        pass
