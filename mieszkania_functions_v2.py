from bs4 import BeautifulSoup
from requests import get
import pandas as pd


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))

def number_of_pages(page, bs):
    link_to_pages = bs.find_all('a', class_="block br3 brc8 large tdnone lheight24")
    for page in link_to_pages:
        ref = page['href']
        num_of_pages = ref.rpartition('page=')[2]
        
    return int(num_of_pages)

def parse_page(URL):
    page = get(URL)
    bs = BeautifulSoup(page.content, "html.parser")
    page_table = []
    for offer in bs.find_all('div', class_="offer-wrapper"):
        footer = offer.find('td', class_="bottom-cell")
        location = footer.find('small', class_="breadcrumb").get_text().strip().split(',')
        if len(location) == 1:
            location.append("-")
        title = offer.find('strong').get_text().strip()
        price = parse_price(offer.find('p', class_="price").get_text().strip())
        link = offer.find('a')['href']
        row = [title, link, price, location[0], location[1]]
        page_table.append(row)

    return page_table

def data_from_city(city, base_URL, num_of_pages):
    df = pd.DataFrame(columns=['name', 'link', 'price', 'city', 'region'])
    for num in range(1,num_of_pages+1):
        print(f"Downloading data from page number {num}, city: {city}")
        URL = f"{base_URL}?page={num}"
        page_table = parse_page(URL)
        df = pd.concat([df, pd.DataFrame(page_table, columns=['name', 'link', 'price', 'city', 'region'])], ignore_index=True)
    return df



