import os
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from sunflower import Sunflower
from sunflower.utils import save_html, load_html
from sunflower.db.models import Category, Product, ProductCategory
from sunflower.db import IntegrityError
from sunflower.settings import logging

from .utils import make_GET_request, regex_categories, regex_products_by_category


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
                msg = str(e) + ": " + f"'{category['name']}', '{category['initials']}'"
                logging.warning(msg)
            else:
                categories.append(c)
        return categories

    def get_products_by_category(self, category, page=1):
        return regex_products_by_category(category, page)

    def get_products(self, save=False):
        categories = set(Category.select().where(Category.parent == None).limit(10))
        products = list()
        for category in categories:
            page = 1
            while True:
                products_per_page = self.get_products_by_category(category, page=page)
                if len(products_per_page) == 0:
                    break
                for product in products_per_page:
                    try:
                        p = Product.create(
                            name=product["name"],
                            url=product["url"]
                        )
                        ProductCategory.create(product=p, category=category)
                    except IntegrityError as e:
                        msg = str(e) + ": " + f"'{product['name']}', '{product['url']}'"
                        logging.warning(msg)
                    else:
                        products.append(p)
                page += 1
        return products
    
    def get_product_reviews(self, product):
        pass

    def get_product_reviews_by_url(self, product_url):
        pass
