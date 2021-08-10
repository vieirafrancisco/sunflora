from pprint import pprint

from sunflower.base import BaseSunflower
from sunflower.db.models import Category, Product, Review

from sunflower.marketplaces.mglu.crawlers import (
    CategoryCrawler,
    ProductCrawler,
    ReviewCrawler,
)


class MagazineLuizaSunflower(BaseSunflower):
    def __init__(self):
        super().__init__(marketplace_url="https://www.magazineluiza.com.br/")

    def load_categories(self):
        crawler = CategoryCrawler(self.marketplace_url)
        categories = list()
        for row in crawler.load():
            category = Category.create_if_not_exist(row)
            if category is not None:
                categories.append(category)
        return categories

    def load_products(self):
        categories = set(Category.select().where(Category.parent == None).limit(10))
        products = list()
        for category in categories:
            page = 1
            while True:
                crawler = ProductCrawler(category.url, page=page)
                products_per_page = crawler.load()
                if len(products_per_page) == 0:
                    break
                for row in products_per_page:
                    row["category"] = category
                    product = Product.create_if_not_exist(row)
                    if product is not None:
                        products.append(product)
                page += 1
        return products

    def load_product_reviews(self, product_id):
        product = Product.select().where(Product.id == product_id).first()
        crawler = ReviewCrawler(product.url, page=1)
        reviews = list()
        for row in crawler.load():
            row["product"] = product
            review = Review.create_if_not_exist(row)
            if review is not None:
                reviews.append(review)
        # TODO: pagination
        return reviews
