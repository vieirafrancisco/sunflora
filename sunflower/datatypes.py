from typing import Type


class Product:
    def __init__(self, name, url, num_reviews=0, mean_rate=0, price=None):
        self.name = name
        self.url = url
        self.num_reviews = num_reviews
        self.mean_rate = mean_rate
        self.price = price

    def __str__(self):
        return f"Product(name: {self.name})"


class Company:
    def __init__(self, name, url, categories):
        self.name = name
        self.url = url
        self.categories = categories

    @staticmethod
    def category_url_pattern(category: str) -> str:
        return f"http://fake_url_pattern.tech/category/{category}"

    @staticmethod
    def get_company(company_name: str) -> Type(Company):
        pass
