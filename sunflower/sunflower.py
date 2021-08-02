from abc import ABC, abstractmethod


class Sunflower(ABC):
    def __init__(self, marketplace_url):
        self.marketplace_url = marketplace_url

    @abstractmethod
    def get_categories(self):
        pass

    @abstractmethod
    def get_products(self):
        pass
    
    @abstractmethod
    def get_product_reviews(self, product_id):
        pass
