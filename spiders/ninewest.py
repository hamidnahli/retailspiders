import requests
import json
from utils import get_ld_json


class Ninewest:

    @staticmethod
    def parse_json(ld: json):
        return {
            'sku': ld['sku'],
            'title': ld['name'],
            'description': ld['description'],
            'price': ld['offers']['price'],
            'currency': ld['offers']['priceCurrency'],
            'price'  : ld['offers']['price'],
            'availability': ld['offers']['availability'],
            'url': ld['offers']['url'],
            'priceValidUntil': ld['offers']['priceValidUntil'],
            'mpn': ld['mpn'],
            'brand': ld['brand'],
            'image': ld['image'],
            "seller_name": ld['offers']['seller']['name'],
        }

    @classmethod
    def product_info(cls, product_url):
        response = requests.get(product_url)
        ld_json = get_ld_json(response)
        data = cls.parse_json(ld_json)
        data['product_url'] = product_url
        return data


p = Ninewest()
info = p.product_info('https://ninewest.com/collections/currently-coveting/products/polka-slingback-heeled-sandals-in-clear')
print(info)