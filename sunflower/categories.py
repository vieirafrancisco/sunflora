import requests
from bs4 import BeautifulSoup

URL = "https://www.magazineluiza.com.br/"

html = requests.get(URL).text
soup = BeautifulSoup(html, "html.parser")

links = soup.find_all("a", {"class": "link-of-menu"})

for link in links[:5]:
    print(link)
