from sunflower.base import BaseCrawler
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer


class CategoryCrawler(BaseCrawler):
    def __init__(self, url):
        super().__init__(url, CategorySerializer)

    def load(self):
        categories = self.find_all("a", {"class": "link-of-menu"}, href=True)
        return list(filter(lambda x: x, categories))


class ProductCrawler(BaseCrawler):
    def __init__(self, url, page=1):
        url = f"{url}?page={page}"
        super().__init__(url, ProductSerializer)

    def load(self):
        products = self.find("ul", {"role": "main"})
        return list(filter(lambda x: x, products))


class ReviewCrawler(BaseCrawler):
    def __init__(self, url, page=1):
        url = f"{url}?page={page}"
        super().__init__(url, ReviewSerializer)
    
    def load(self):
        reviews = self.find("div", {"class": "wrapper-reviews__list"})
        return list(filter(lambda x: x, reviews))
