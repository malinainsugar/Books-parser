import requests
from bs4 import BeautifulSoup as bs

NOVELTY_URL = "https://www.chitai-gorod.ru/catalog/collections/novelty"

def parsing_books():
    page = requests.get(url=NOVELTY_URL)
    html = page.text
    soup = bs(html, "lxml")
    product_card_list = soup.find_all("article", attrs={"class" : "product-card"})

    books_list = []
    for book in product_card_list:
        link = 'https://www.chitai-gorod.ru' + book.find("a", attrs={"class" : "product-card__title"}).get('href')
        name = book.find("div", attrs={"class" : "product-title__head"}).get_text().strip()
        author = book.find("div", attrs={"class" : "product-title__author"}).get_text().strip()
        price = int(book.find("div", attrs={"class" : "product-price__value"}).get_text().strip().replace("₽", "").replace("\xa0", ""))

        book = requests.get(url=link)
        book_html = book.text 
        book_soup = bs(book_html, "lxml")

        book = {
            'name' : name,
            'author' : author,
            'publisher' : book_soup.find("a", itemprop="publisher").get_text().strip(),
            'year' : int(book_soup.find("span", itemprop="datePublished").get_text()),
            'page_count' : int(book_soup.find("span", itemprop="numberOfPages").get_text()),
            'price' : price,
            'description' : book_soup.find("div", itemprop="description").get_text().strip().replace("\xa0", ""),
            'link' : link,
            'product_id' : int(book_soup.find("span", attrs={"class" : "product-detail-characteristics__item-value"}).get_text().strip())
        }
        books_list.append(book)
    return books_list
