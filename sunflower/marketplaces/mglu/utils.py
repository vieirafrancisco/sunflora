import os
import re
import time
import requests
from pprint import pprint

from bs4 import BeautifulSoup
from bs4.element import Tag

from sunflower.settings import logging, session


def regex_categories(url):
    html = session.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", {"class": "link-of-menu"}, href=True)

    categories = list()
    for link in links:
        category = re.findall(r"^%s(.+)\/l\/(.+)\/$" % url, link["href"])
        subcategory = re.findall(r"^%s(.+)\/(.+)\/s\/(.+)\/(.+)\/$" % url, link["href"])
        if len(category) > 0:
            category = category[0]
            categories.append(
                {
                    "name": category[0],
                    "initials": category[1],
                    "url": link["href"],
                    "parent": None,
                }
            )
        if len(subcategory) > 0:
            subcategory = subcategory[0]
            categories.append(
                {
                    "name": subcategory[0],
                    "initials": subcategory[3],
                    "url": link["href"],
                    "parent": {"name": subcategory[1], "initials": subcategory[2]},
                }
            )
    return categories


def regex_products_by_category(category, page):
    products = list()
    logging.debug(
        f"Initialize 'regex_products_by_category'. Category: {category.name}, Page: {page}."
    )
    url = f"{category.url}?page={page}"
    html = session.get(url).text

    soup = BeautifulSoup(html, "html.parser")
    product_list = soup.find("ul", {"role": "main"})

    if product_list is None or "Nenhum produto encontrado" in product_list:
        return []
    items = product_list.contents
    for item in items:
        products.append({"name": item.contents[-1].h3["title"], "url": item["href"]})
    return products


def regex_product_reviews(product, page=1):
    reviews = list()
    logging.debug(
        f"Initialize 'regex_product_reviews'. Product: {product.name}, Page: {page}."
    )
    url = f"{product.url}?page={page}"
    html = session.get(url).text

    soup = BeautifulSoup(html, "html.parser")
    reviews_list = soup.find("div", {"class": "wrapper-reviews__list"})

    if reviews_list is None:
        return []

    items = filter(lambda x: isinstance(x, Tag), reviews_list.contents)
    for item in items:
        review = tree(item)
        text_content = review["product-review__text-content"]
        title = review.get("product-review__text-content--title", [("", "")])[0][0]
        reviews.append(
            {
                "rating": len(
                    list(filter(lambda x: x[1], review["rating-percent__full-star"]))
                ),
                "username": text_content[0][0],
                "relative_data": review["product-review__text-highlight"][0][0],
                "title": title,
                "text": text_content[1][0] if len(text_content) > 1 else "",
                "is_recommended": review["strong"][0][0] == "Sim",
                "thumbs_up": int(
                    review["product-review__text-highlight"][1][0]
                    .replace("(", "")
                    .replace(")", "")
                ),
                "thumbs_down": int(
                    review["product-review__text-highlight"][2][0]
                    .replace("(", "")
                    .replace(")", "")
                ),
                "cost_benefit_rate": float(
                    review["product-review__rating-number"][0][0]
                ),
                "general_quality_rate": float(
                    review["product-review__rating-number"][1][0]
                ),
            }
        )
    return reviews


def update_state(state, d):
    tmp_state = state.copy()
    for key, value in d.items():
        if key not in tmp_state.keys():
            tmp_state[key] = list()
        if isinstance(value, list):
            for x in value:
                tmp_state[key].append(x)
        else:
            tmp_state[key].append(value)
    return tmp_state


def tree(tag):
    contents = list(tag.contents)
    if len(contents) == 0:
        return {}
    value = contents[0]
    state = {}
    if value != " ":
        key = tag.get("class") or tag.name
        if tag.get("class") is not None:
            key = key[0]
        return {key: (value, tag.get("style", ""))}

    for content in contents:
        if isinstance(content, Tag):
            result = tree(content)
            state = update_state(state, result)
    return state
