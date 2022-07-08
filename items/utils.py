import json
import os
import requests
from typing import Any, Dict
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from usp.tree import sitemap_tree_for_homepage
from celery import Celery

from items.debugging import app_logger as log
from items.proxy import start_session

load_dotenv()

app = Celery('tasks', broker='sqs://', broker_transport_options={'region': 'us-east-2'})

# return all product urls using the website's robots.txt
# identifier is the keyword that identify a product url
@app.task
def parse_robots_txt(url, identifier=None):
    urls = []
    tree = sitemap_tree_for_homepage(url)
    for page in tree.all_pages():
        urls.append(page.url)
    if identifier:
        urls = [url for url in urls if identifier in url]
    return urls

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

def parse_bazaarvoice_reviews(product_id,offset=0):
    url = f'https://api.bazaarvoice.com/data/batch.json?passkey=thvpbov9ywkkl4nkhbeq0wm1i&apiversion=5.5&displaycode=15372-en_us&resource.q0=reviews&filter.q0=isratingsonly%3Aeq%3Afalse&filter.q0=productid%3Aeq%3A{product_id}&filter.q0=contentlocale%3Aeq%3Aen*%2Cen_US&sort.q0=submissiontime%3Adesc&stats.q0=reviews&filteredstats.q0=reviews&include.q0=authors%2Cproducts%2Ccomments&filter_reviews.q0=contentlocale%3Aeq%3Aen*%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen*%2Cen_US&filter_comments.q0=contentlocale%3Aeq%3Aen*%2Cen_US&limit.q0=100&offset.q0={offset}&limit_comments.q0=20&callback=bv_351_1793'
    response = requests.get(url).text
    data = response.replace('bv_351_1793(','')[:-1]
    data = json.loads(data)
    totalResults = data['BatchedResults']['q0']['TotalResults']
    return [data,totalResults]