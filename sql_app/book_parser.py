import requests
from bs4 import BeautifulSoup as bs

PRODUCT_URL = "https://www.chitai-gorod.ru/catalog/collections/novelty"

def parsing_all_books():
    page = requests.get(url=PRODUCT_URL)
    html = page.text
    soup = bs(html, "lxml")


booksList = soup.find_all("article", attrs={"class" : "product-card"})
for book in booksList:
    title = book.find("div", attrs={"class" : "product-title__head"}).get_text().strip()
    price = int(book.find("div", attrs={"class" : "product-price__value"}).get_text().strip().replace("₽", "").replace("\xa0", ""))
    element = session.query(Books).filter(Books.name == title)
    if (element.count() == 0):
        session.add(
        Books(
            name = title,
            author = book.find("div", attrs={"class" : "product-title__author"}).get_text().strip(),
            publisher = '',
            year = '',
            pageСount = '',
            price = price,
            description = '',
            link = 'https://www.chitai-gorod.ru/' + book.find("a", attrs={"class" : "product-card__title"}).get('href')
        )
    )
    else:
        element.first().price = price
