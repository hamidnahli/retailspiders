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

def parse_yotpo_reviews():
    product_reviews = []
    key = os.getenv('key')
    product_url = f'https://api.yotpo.com/v1/reviews/{key}/filter.json'
    headers = {
        'Content-Type': 'application/json'
    }

    payload = json.dumps({

        "domain_key": "lidstar",
        "crfs": [],
        "sortings": [
        {
            "sort_by": "date",
            "ascending": False,
        }
        ],
        "page": 1,
        "per_page": 150,
        })

    response = requests.post(product_url,data=payload,headers=headers)
    data = response.json()
    id_product=data['response']['products'][0]['id']
    rtype=data['response']['product_tags'][0]['tag']
    pages_total = data['response']['pagination']['total']
    pages_total = pages_total//150

    for page in range(0,pages_total):
        payload = json.dumps({
                                "domain_key": "lidstar",
                                "crfs": [],
                                "sortings": [
                                {
                                    "sort_by": "date",
                                    "ascending": False,
                                }
                                ],
                                "page": page,
                                "per_page": 150,
                            })
        response = requests.post(product_url,data=payload,headers=headers)
        data = response.json()

        for ele in data['response']['reviews']:
            review_comment = ele['content']
            review_headline = ele['title']
            review_date = ele['created_at']
            review_author = ele['user']['display_name']
            review_thumbs_up = ele['votes_up']
            review_thumbs_down = ele['votes_down']

            review = {
                'rtype':rtype,
                'id':id_product,
                'date': review_date,
                'author': review_author,
                'header': review_headline,
                'body': review_comment,
                'thumbs_up': review_thumbs_up,
                'thumbs_down': review_thumbs_down,
                'pages_total': pages_total
            }

            product_reviews.append(review)
    return product_reviews

    
