import requests
import json
from utils import get_ld_json

class Clinique:

    @staticmethod

    def parse_json(ld: json):
        if ld.get('aggregateRating'):
            ratingCount = ld.get('aggregateRating').get('ratingCount')
            ratingValue = ld.get('aggregateRating').get('ratingValue')
        else:
            ratingCount = None
            ratingValue = None
        return {
            'url':ld['url'],
            'sku': ld['sku'],
            'title': ld['name'],
            'description': ld.get('description'),
            'ratingValue': ratingValue,
            'ratingCount ': ratingCount,
            'seller_name' : ld['offers'][0]['seller']['name'],
            'seller_type': ld['offers'][0]['seller']['@type'],
            'offer_image': ld['offers'][1]['image'],
            'priceCurrency': ld['offers'][1]['priceCurrency'],
            'price': ld['offers'][1]['price'],
            'availability': ld['offers'][1]['availability'],
            'offer_price': ld['offers'][2]['price'],
            'brand': ld['brand'],
            'brand_name': ld['brand']['image'],
            'brand_url':ld['brand']['url'],
            'image': ld['image'],
        }

    @classmethod
    def product_info(cls, product_url):
        response = requests.get(product_url)
        ld_json = get_ld_json(response)
        data = cls.parse_json(ld_json)
        data['product_url'] = product_url
        return data


p = Clinique()
info = p.product_info('https://www.clinique.com/product/4034/87057/skincare/serum/clinique-smart-clinical-repairtm-wrinkle-correcting-serum?size=1.7_oz._%2F_50_ml')
print(info)
