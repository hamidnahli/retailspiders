import requests
import json
from utils import get_ld_json

class   Anthropologie:
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
    
    @staticmethod
    def parse_json(ld: json):
        if ld.get('aggregateRating'):
            product_ratingCount = ld.get('aggregateRating').get('ratingCount')
            product_ratingValue = ld.get('aggregateRating').get('ratingValue')
        else :
            product_ratingCount = None
            product_ratingValue = None
        return {
            'name' : ld['name'],
            'sku' : ld['sku'],
            'seller' : ld['offers']['seller']['name'],
            'description' : ld.get('description'),
            'Currency' : ld['offers']['priceCurrency'],
            'image' : ld['image'],
            'price' : ld['offers']['offers'][0]['price'],
            'category' : ld['category'],
            'product_ratingCount' : product_ratingCount,
            'product_ratingValue' : product_ratingValue,
        }
    
    @classmethod
    def product_info(cls, product_url):
        response = requests.get(product_url, headers = cls.global_headers())
        ld_json = get_ld_json(response)
        data = cls.parse_json(ld_json)
        return data

p = Anthropologie()
print(p.product_info('https://www.anthropologie.com/shop/facial-rounds?color=000&recommendation=home-hpg-tray-1-sfrectray-homepagetrendingmostpurchased&type=STANDARD&size=One%20Size&quantity=1'))
