from bs4.element import Tag

from sunflower.base import BaseSerializer
from sunflower.settings import logging

from .utils import search_category, tree


class CategorySerializer(BaseSerializer):
    def __init__(self, item, many=False):
        super().__init__(item, many=many)

    def serialize(self, item):
        category = search_category(item)
        if category:
            return {
                "name": category["name"],
                "initials": category["initials"],
                "url": item["href"],
                "parent": category["parent"],
            }
        return {}


class ProductSerializer(BaseSerializer):
    def __init__(self, item, many=False):
        super().__init__(item, many=many)

    def serialize(self, item):
        try:
            return {"name": item.contents[-1].h3["title"], "url": item["href"]}
        except Exception as e:
            logging.error(e)
        return {}


class ReviewSerializer(BaseSerializer):
    def __init__(self, item, many=False):
        super().__init__(item, many=many)

    def serialize(self, item):
        if item is None or not isinstance(item, Tag):
            return {}
        review = tree(item)
        text_content = review["product-review__text-content"]
        title = review.get("product-review__text-content--title", [("", "")])[0][0]
        return {
            "rating": len(
                list(filter(lambda x: x[1], review["rating-percent__full-star"]))
            ),
            "username": text_content[0][0],
            "relative_date": review["product-review__text-highlight"][0][0],
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

