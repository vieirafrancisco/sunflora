# import time
import os
import sys
# import random
import requests
import logging
import pickle
from pprint import pprint

from bs4 import BeautifulSoup
from bs4.element import NavigableString
# from selenium.webdriver import Firefox
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from sunflower import settings
from sunflower.db.models import Review


class ReviewsParser:
   def __init__(self, reviews_soup):
      self.reviews_soup = reviews_soup

   @property
   def comments(self):
      return self.reviews_soup.find_all("div", {"class": "wrapper-review__comment"})


def prep_reviews_tag(reviews_tag: object) -> list:  # return list[Review]
   reviews = list()
   return []
   for review_comment in reviews_tag.find_all("div", {"class": "wrapper-review__comment"}):
      pass
      # reviews.append(Review(
      #    rating=None,
      #    username="",
      #    relative_data="",
      #    title="",
      #    text="",
      #    is_recommended=True,
      #    thumbs_up=0,
      #    thumbs_down=0,
      #    cost_benefit_rate=0,
      #    general_quality_rate=0
      # ))

def get_reviews_by_product_url(url: str) -> list:  # return list[Review]
   html = requests.get(url).text
   soup = BeautifulSoup(html, "html.parser")
   
   tag = soup.find("div", {"class": "wrapper-reviews__list"})
   
   reviews = prep_reviews_tag(tag)
   logging.info(f"Response: {len(reviews)} reviews in total!")

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
      return {key: value}
   for content in contents:
      if type(content) != NavigableString:
         result = tree(content)
         #print(result)
         state = update_state(state, result)
   return state


def save_html(file_name, url):
   html = str(requests.get(url).text).encode()
   with open(f"sunflower/tmp/{file_name}.html", "wb") as f:
      f.write(html)

def load_html(file_name):
   with open(f"sunflower/tmp/{file_name}.html", "rb") as f:
      return f.read().decode()

def test():
   html = load_html("test_data")
   soup = BeautifulSoup(html, "html.parser")
   tag = soup.find("div", {"class": "wrapper-reviews__list"})
   reviews = list()
   if tag is not None:
      for child in tag.contents:
         if type(child) != NavigableString:
            reviews.append(tree(child))
   pprint(reviews[0])
   


# with Firefox(executable_path='drivers/geckodriver') as browser:
#    browser.get(URL)
#    index = 1
#    while index <= MAX_ITER:
#       html = browser.page_source
#       soup = BeautifulSoup(html, "html.parser")

#       reviews = soup.find_all("div", {"class": "wrapper-review__comment"})

#       logging.info(f"Page: {index} with {len(reviews)} reviews in total!")
#       index += 1

#       timing = random.randint(120, 130)
#       logging.debug(f"Sleeping for {timing} seconds.")
#       time.sleep(timing)

#       try:
#          elem = browser.find_element_by_xpath('//button[normalize-space()="Carregar mais avaliações"]')
#          browser.execute_script("arguments[0].click();", elem)
#       except NoSuchElementException:
#          logging.error('Elemento não existe!')
#          sys.exit(1)
#       except ElementClickInterceptedException as e:
#          logging.error(e)
#          sys.exit(1)
