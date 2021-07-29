import os
import re
import time
import requests
from pprint import pprint

from bs4 import BeautifulSoup

from sunflower.marketplaces.config import CACHE_DIR
from sunflower.utils import save_html, load_html
from sunflower.settings import logging


def make_GET_request(url, file_name, cache=True):
    if cache and file_name in os.listdir(CACHE_DIR):
        html = load_html(os.path.join(CACHE_DIR, file_name))
    else:
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception(f"Request to url {url} failed.")
        html = resp.text
        if file_name:
            save_html(os.path.join(CACHE_DIR, file_name), html=html)
    return html

def regex_categories(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", {"class": "link-of-menu"}, href=True)
    url = "https://www.magazineluiza.com.br/"
    categories = list()
    for link in links:
        category = re.findall(r"^%s(.+)\/l\/(.+)\/$" % url, link["href"])
        subcategory = re.findall(r"^%s(.+)\/(.+)\/s\/(.+)\/(.+)\/$" % url, link["href"])
        if len(category) > 0:
            category = category[0]
            categories.append({
                "name": category[0],
                "initials": category[1],
                "url": link["href"],
                "parent": None,
            })
        if len(subcategory) > 0:
            subcategory = subcategory[0]
            categories.append({
                "name": subcategory[0],
                "initials": subcategory[3],
                "url": link["href"],
                "parent": {
                    "name": subcategory[1],
                    "initials": subcategory[2]
                }
            })
    return categories

def regex_products_by_category(category, page):
    products = list()
    logging.debug(f"Initialize 'regex_products_by_category'. Category: {category.name}, Page: {page}.")
    url = f"{category.url}?page={page}"
    file_name = f"mglu_products_by_category_{category.name}_page_{page}.html"
    if file_name in os.listdir(CACHE_DIR):
        html = load_html(os.path.join(CACHE_DIR, file_name))
    else:
        logging.info("Sleeping for 30 seconds.")
        time.sleep(30)
        html = make_GET_request(url, file_name, cache=True)

    soup = BeautifulSoup(html, "html.parser")
    product_list = soup.find("ul", {"role": "main"})
    
    if product_list is None or "Nenhum produto encontrado" in product_list:
        return []
    items = product_list.contents
    for item in items:
        products.append({
            "name": item.contents[-1].h3["title"],
            "url": item["href"]
        })
    return products
