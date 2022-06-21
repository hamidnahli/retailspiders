import requests
import json
from utils import get_ld_json

class   Fragrancenet:

    @staticmethod
    def parse_json(ld: json):
        return {
            'title' : ld[0]['name'],
            'sku' : ld[0]['sku'],
            'brand' : ld[0]['brand']['name'],
            'image' : ld[0]['image'],
            'price' : ld[0]['offers']['price'],
            'Currency' : ld[0]['offers']['priceCurrency'],
            #'description' : ld.get('description'),
            #'seller' : ld['offers'][0]['seller']['name'],
            
        }

    @classmethod
    def product_info(cls, product_url):
        response = requests.get(product_url)
        ld_json = get_ld_json(response)
        data = cls.parse_json(ld_json)
        return data

p = Fragrancenet()
print(p.product_info('https://www.fragrancenet.com/perfume/dolce-and-gabbana/d-and-g-light-blue/edt#120682'))
