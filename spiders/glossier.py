import requests
import json
from utils import get_ld_json

class Glossier:

    @staticmethod

    def parse_json(ld: json):
        return {
          #'sku': ld['sku'],
            'title': ld['name'],
            'description': ld.get('briefDescription'),
            'price': ld['offers']['price'],
            'currency': ld['offers']['priceCurrency'],
             'offer_item': ld['offers']['itemCondition'],
             'id' : ld['@id'],
             'availability':ld['offers']['availability'],
            'brand': ld['brand'],
            'image': ld['image'],
        }
        

    @classmethod
    def product_info(cls, product_url):
        response = requests.get(product_url)
        ld_json = get_ld_json(response)
        data = cls.parse_json(ld_json)
        data['product_url'] = product_url
        return data


p = Glossier()
info = p.product_info('https://www.glossier.com/products/makeup-set-balm-dotcom')
print(info)
