import requests

from utils import get_ld_json


class NineWest:

    def __init__(self, product_url):
        self.product_url = product_url

    def product_info(self):
        response = requests.get(self.product_url)
        ld_json = get_ld_json(response)
        return ld_json

p = NineWest('https://ninewest.com/products/speakup-almond-toe-flats-in-black-floral')

print(p.product_info())
