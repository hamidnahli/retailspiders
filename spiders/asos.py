import requests
import json
from utils import get_ld_json

class   Asos:
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
        return {
            'title' : ld['name'],
            'sku' : ld['sku'],
            'description' : ld.get('description'),
            'image' : ld['image'],
            'url' : ld['url'],
            'brand' : ld['brand']['name'],
        }

    @classmethod
    def product_info(cls, product_url):
        response = requests.get(product_url, headers = cls.global_headers())
        ld_json = get_ld_json(response)
        data = cls.parse_json(ld_json)
        return data

p = Asos()
print(p.product_info('https://www.asos.com/truffle-collection/truffle-collection-extra-chunky-sliders-in-charcoal/prd/201590566?colourWayId=201590567&cid=1935'))
