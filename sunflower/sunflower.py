from abc import ABC, abstractmethod


class Sunflower(ABC):
    def __init__(self, marketplace_url):
        self.marketplace_url = marketplace_url

    @abstractmethod
    def get_categories(self, save=False, cache=True):
        pass

    @abstractmethod
    def get_products_by_category(self, category, page=1):
        pass

    @abstractmethod
    def get_products(self, save=False):
        pass
    
    @abstractmethod
    def get_product_reviews(self, product):
        pass

    @abstractmethod
    def get_product_reviews_by_url(self, product_url):
        pass
