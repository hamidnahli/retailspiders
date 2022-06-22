import json
import os
from typing import Any, Dict

from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode

import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from items.debugging import app_logger as log

load_dotenv()


def get_next_url(url: str, param: str, nxt: int):
    url_parse = urlparse(url)
    query = url_parse.query
    url_dict: Dict[str, Any] = dict(parse_qsl(query))
    if isinstance(url_dict[param], list):
        page = int(url_dict[param][0]) + nxt
    else:
        page = int(url_dict[param]) + nxt
    params = {param: page}
    url_dict.update(params)
    url_new_query = urlencode(url_dict)
    url_parse = url_parse._replace(query=url_new_query)
    next_url = urlunparse(url_parse)
    return next_url


def get_ld_json(response: requests.Response):
    soup = BeautifulSoup(response.content, 'html.parser')
    lds = soup.findAll('script', {'type': 'application/ld+json'})
    if lds:
        for ld in lds:
            if "Product" in ld.text:
                return json.loads(ld.text)
    else:
        log.info(f'ld+json not found for {response.url}')
    return None


# This should be a standard template for all shopify websites
def get_shopify_variants(response: requests.Response):
    soup = BeautifulSoup(response.content, 'html.parser')
    scripts = soup.findAll('script')
    script = [ele.text for ele in scripts if '"variants":' in ele.text][0]
    str_json = [ele for ele in script.split(';') if '"variants":' in ele][0].strip()
    str_json = str_json.replace('var meta = ', '')
    data = json.loads(str_json)
    variants = data['product']['variants']
    rid = data['product']['id']
    rtype = data['product']['type']
    return rid, rtype, variants


# Parsing reviews from stamped.oo
def parse_stamped_reviews(rid, rtype, product_name, product_sku):
    reviews = []
    review_containers = True
    api_key = os.getenv('ninewest_stamped_api')
    store_key = os.getenv('ninewest_stamped_store')
    page = 1
    rating = 0
    count = 0
    while review_containers:
        url = f'https://stamped.io/api/widget?productId={rid}&productName={product_name}&productType={rtype}&productSKU={product_sku}&page={page}&apiKey={api_key}&storeUrl={store_key}&take=16&sort=rece'
        response = requests.get(url)
        data = response.json()
        rating = data['rating']
        count = data['count']
        html_reviews = data['widget'].strip()
        soup = BeautifulSoup(html_reviews, 'html.parser')
        review_containers = soup.findAll('div', {'class': 'stamped-review'})
        if review_containers:
            for review_container in review_containers:
                review_date = review_container.find('div', {'class': 'created'}).text
                review_author = review_container.find('strong', {'class': 'author'}).text
                review_location = review_container.find('div', {'class': 'review-location'}).text
                review_header = review_container.find('h3', {'class': 'stamped-review-header-title'}).text
                review_body = review_container.find('p', {'class': 'stamped-review-content-body'}).text
                review_thumbs_up = review_container.find('i', {'class': 'stamped-fa stamped-fa-thumbs-up'}).text.strip()
                review_thumbs_down = review_container.find('i',
                                                           {'class': 'stamped-fa stamped-fa-thumbs-down'}).text.strip()

                review = {
                    'date': review_date,
                    'author': review_author,
                    'location': review_location,
                    'header': review_header,
                    'body': review_body,
                    'thumbs_up': review_thumbs_up,
                    'thumbs_down': review_thumbs_down
                }
                reviews.append(review)
        page += 1
    return rating, count, reviews