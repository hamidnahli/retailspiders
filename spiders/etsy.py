import requests
import json
from utils import get_ld_json

class Etsy:
    @staticmethod
    def parse_json(ld: json):
        if ld.get('aggregateRating'):
            product_ratingCount = ld.get('aggregateRating').get('ratingCount')
            product_ratingValue = ld.get('aggregateRating').get('ratingValue')
        else:
            product_ratingCount = None
            product_ratingValue = None
        return {
            'url':ld['url'],
            'sku': ld['sku'],
            'title': ld['name'],
            'description': ld.get('description'),
            'product_ratingValue': product_ratingValue,
            'product_ratingCount ': product_ratingCount,
            'image_autor':ld['image'][0]['author'],
            'currency': ld['offers']['priceCurrency'],
            'lowPrice':ld['offers']['lowPrice'],
            'highPrice':ld['offers']['highPrice'],
            'availability': ld['offers']['availability'],
            'offers_type': ld['offers']['@type'],
            'brand': ld['brand'],
            'image': ld['image'],
            'category': ld['category'],
            'logo': ld['logo'],
        }

    @classmethod
    def product_info(cls, product_url):
        response = requests.get(product_url)
        ld_json = get_ld_json(response)
        data = cls.parse_json(ld_json)
        data['product_url'] = product_url
        return data


p =Etsy()
info = p.product_info('https://www.etsy.com/fr/listing/1048950291/tasse-avec-liste-de-dates-personnalisees?ref=anchored_listing')
print(info)