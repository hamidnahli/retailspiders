from numpy import prod
import requests
import json
from utils import get_ld_json

class Rei:

    @staticmethod
    def parse_json(ld: json):
        return {
            'name' : ld['name'],
            'description' : ld.get('description'),
            'brand' : ld['brand']['name'],
            'price' : ld['offers'][0]['price'],
            'image' : ld['image'],
            'currency' : ld['offers'][0]['priceCurrency'],
            'sku' : ld['sku'],
            'category' : ld['category'],
            'url' : ld['offers'][0]['url'],
        }
    
    @classmethod
    def product_info(cls, product_url):
        response = requests.get(product_url)
        ld_json = get_ld_json(response)
        data = cls.parse_json(ld_json)
        return data

pi = Rei()
print(pi.product_info('https://www.rei.com/product/195355/athleta-pranayama-wrap-womens'))