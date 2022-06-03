from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import datetime


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))

def number_of_pages(page, bs):
    link_to_pages = bs.find_all('a', class_="css-1mi714g")
    for page in link_to_pages:
        ref = page['href']
        num_of_pages = ref.rpartition('page=')[2]
        
    return int(num_of_pages)

def parse_page(URL):
    page = get(URL)
    bs = BeautifulSoup(page.content, "html.parser")
    page_table = []
    
    for offer in bs.find_all('div', class_="css-19ucd76"):
        
        location = offer.find('p', class_="css-p6wsjo-Text eu5v0x0")
        if location is not None:
            location = offer.find('p', class_="css-p6wsjo-Text eu5v0x0").get_text().strip().split(' - ')[0]
            date = offer.find('p', class_="css-p6wsjo-Text eu5v0x0").get_text().strip().split(' - ')[1] 
        else: 
            continue
        
        title = offer.find('h6', class_='css-v3vynn-Text eu5v0x0').get_text()
        price = float(offer.find('p', class_="css-l0108r-Text eu5v0x0").get_text().strip().split('zł')[0].replace(' ', '').replace(',', '.'))
        link = offer.find('a', class_="css-1bbgabe")['href']
        row = [title, link, price, location, date]
        page_table.append(row)
    return page_table

def data_from_city(city, base_URL, num_of_pages):
    df = pd.DataFrame(columns=['name', 'link', 'price', 'city', 'date'])
    for num in range(1,num_of_pages+1):
        URL = f"{base_URL}?page={num}"
        page_table = parse_page(URL)
        df = pd.concat([df, pd.DataFrame(page_table, columns=['name', 'link', 'price', 'city', 'date'])], ignore_index=True)
    return df


