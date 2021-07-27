from typing import Type

from bs4 import BeautifulSoup

from sunflower.datatypes import Product, Company


class ProductCrawler:
    def __init__(self):
        self._product_list = []

    @property
    def product_list(self) -> list:
        return self._product_list

    @staticmethod
    def parser(product: str) -> Type(Product):
        return Product("default", "http://fake_url.tech")

    def scrape(self):
        pass


class MagazineLuizaProductCrawler(ProductCrawler):
    def __init__(self):
        super().__init__()
        self.company = Company.get_company("magazine-luiza")

    @property
    def product_list(self, force_scrape=False) -> list:
        if self._product_list == [] or force_scrape:
            self._product_list = list(self.scrape())
        return self._product_list

    @staticmethod
    def parser(product):
        return super().parser()

    def save(self, product):
        if product.name not in self.set_products.keys():
            self.set_products[product.name] = product

    def parse_and_save(self, products):
        for product in products:
            parsed_product = MagazineLuizaProductCrawler.parser(product)
            self.save(parsed_product)

    def scrape(self, pagination=1):
        if pagination < 1:
            raise Exception("Pagination must be a positive number > 0.")
        for page in range(pagination):
            url = f"{self.company.url}?page={page}"
            soup = BeautifulSoup(url, "html.parser")
            products = soup.find_all("div", {"class": "product"})
            self.parse_and_save(products)
            # TODO: make pagination click button

