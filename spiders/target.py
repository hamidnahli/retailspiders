import requests
import json
from utils import get_ld_json


class Target:
    reviews = []
    info = None

    @staticmethod
    def _parse_json(ld: json):
        ld = ld['@graph'][0]
        return {
            'sku': ld['sku'],
            'title': ld['name'],
            'description': ld['description'],
            'price': ld['offers']['price'],
            'currency': ld['offers']['priceCurrency'],
            'brand': ld['brand'],
            'image': ld['image'],
        }

    @classmethod
    def product_info(cls, product_url):
        response = requests.get(product_url)
        ld_json = get_ld_json(response)
        data = cls._parse_json(ld_json)
        data['url'] = product_url
        return data

    def product_review(self):
        ...
