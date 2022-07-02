import json
import os
from typing import Any, Dict
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from items.debugging import app_logger as log
load_dotenv()

def global_headers():
    return {
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,de;q=0.6',
            }

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

