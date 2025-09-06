import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0 Safari/537.36"
}

def get_html(link):
    opening_link = requests.get(link, headers = headers)
    return bs(opening_link.text, 'html.parser')

def get_next_page(review_section):
    last_idx = len(review_section) -1
    next_page = "https://www.flipkart.com" +review_section[last_idx].find_all('a')[-1]['href']
    return next_page

def get_product_details(product_link):
    product_page = requests.get(product_link, headers = headers)

    # Parsing the html data -> So that it can be easily searchable
    product_html = bs(product_page.text, 'html.parser')

    # Product's image
    product_image = product_html.find_all('div',{"class": "_4WELSP _6lpKCl"})[0].find_all('img')[0]["src"]

    # Product's name
    product_name = product_html.find_all('div',{"class": "_4WELSP _6lpKCl"})[0].find_all('img')[0]["alt"]

    return [product_image, product_name]

def get_data(product_link):
    # will store entire data here
    all_data = []

    # TRACKING FOR DUPLICATE PAGE TO AVOID INFINITE LOOP
    visited_pages = set()  

    # Fetching the html data of page
    product_page = requests.get(product_link, headers = headers)

    # Parsing the html data -> So that it can be easily searchable
    product_html = bs(product_page.text, 'html.parser')

    # Fetching the "All Revies Section"
    all_review_section= product_html.find_all('div',{"class": "col pPAw9M"})

    # Fetching links available in "All review Section"
    review_section_links = [all_review_section[0].find_all('a')]
    all_review_page = "https://www.flipkart.com" + review_section_links[0][-1]['href']

    # THIS IS PAGE 1 
    review_page_html = get_html(all_review_page)

    while True:
        # FETCHING REVIEW SECTION
        review_section = review_page_html.find_all('div',{"class": "cPHDOP col-12-12"})

        # PRINTING THE ALL REVIEWS PRESENT IN THIS PARTICULAR PAGE
        for i in range(len(review_section)):
            try:
                heading = review_section[i].div.div.div.find_all('p')[0].text
                user = review_section[i].div.div.div.find_all('p')[1].text
                rating = review_section[i].div.div.div.div.text[0]
                review =review_section[i].div.div.div.find_all('div',{"class": "ZmyHeo"})[0].text.replace("READ MORE","")
                data = {
                    "user_name": user,
                    "heading": heading,
                    "rating": rating,
                    "review": review
                }

                all_data.append(data)
            except:
                pass

        # NOW FETCHING NEXT PAGE FOR MORE REVIEWS
        try:
            next_page = get_next_page(review_section)
            if not next_page or next_page in visited_pages:
                return all_data   # If None or empty
            
            visited_pages.add(next_page)
        except:
            return all_data
        
        # IF WE SUCCESSFULLY FETCHED NEXT PAGE -> GETTING PARSED HTML
        review_page_html = get_html(next_page)

