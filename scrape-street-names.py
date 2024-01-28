"""A program that scrapes and cleans all street names on the LondonStreetIndex (LSI) into a list.

        generate_urls(): generates a list of the urls used in LSI. Returns url_list.

        scrape_names(url_list): scrapes the names from each website page into a single list. Returns name_list.

        clean_names(name): removes area code from name and adds a period behind 'st ' if those are the first three digits (saint name). Returns name.

        write_txt_file(name_list_clean): writes a text file of all clean street names.

"""
import string
from bs4 import BeautifulSoup
import requests
import re

testing_mode = True

def generate_urls():
    """Creates list of URLs representing the pages listing street names on LSI.url_list returned."""

    #url list represents the 25 pages of street names on LSI, listed alphabetically.
    url_list = []

    for letter in string.ascii_lowercase:
        #There are no streets in the LSI starting with X, so there is no X page. Therefore, an url is generated for every page but X.
        if letter != 'x':
            new_url = f'https://www.londononline.co.uk/streetindex/{letter}/'
            url_list.append(new_url)

    if testing_mode:
        print(f"GENERATE_URLS() TEST:\nList length = {len(url_list)}\nSample = {url_list[0]}")

    return url_list

def scrape_names(url_list):
    """Scrapes through the urls on url_list, then cleans each name and appends to name_list, which is returned."""

    #name_list represents the 24113 names scraped from LSI. Each name has been cleaned (lowercase, no area code, period after 'st').
    name_list =[]

    for url in url_list:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        soup_name_list = soup.find('ul', class_='list-group').find_all('li', class_='list-group-item')

        for name_line in soup_name_list:
            name = name_line.find('a')
            name = name.text
            name_list.append(clean_name(name)) #append cleaned data

    if testing_mode:
        print(f'SCRAPE_NAMES() TEST\nname_list count = {len(name_list)}\nname_list sample = {name_list[3:9]}')

    return name_list

def clean_name(name):
    name = name.lower()
    name = re.sub('( \([a-z0-9]+\))','',name) #remove area code

    #if street name starts with 'st ', indicating a saint name, replace with 'st. ' (makes it easier to filter in filter-street-names.py)
    if name[0:3] == 'st ':
        name = re.sub('st ', 'st. ', name, 1)

    return name


def  write_txt_file(name_list):
    return 0

if __name__ == "__main__":
    url_list = generate_urls()
    name_list = scrape_names(url_list)

