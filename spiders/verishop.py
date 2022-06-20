import requests
import json
from utils import get_ld_json


class Verishop:

    @staticmethod
    def parse_json(ld: json):
        return {
            'sku': ld['sku'],
            'title': ld['name'],
            'description': ld['description'],
            'price': ld['offers']['price'],
            'currency': ld['offers']['priceCurrency'],
            'brand': ld['brand'],
            'image': ld['image'],
            'category': ld['category'],
            "seller_name": ld['offers']['seller']['name'],
        }

    @classmethod
    def product_info(cls, product_url):
        response = requests.get(product_url)
        ld_json = get_ld_json(response)
        data = cls.parse_json(ld_json)
        data['product_url'] = product_url
        return data


p = Verishop()
info = p.product_info('https://www.verishop.com/molly-pepper/marketplace/mona-dress-in-black/p7169305182402?variant_id=41400327405762')
print(info)