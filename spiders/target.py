import requests

from utils import get_ld_json, parse_json


class Target:
    def __init__(self, product_url):
        self.product_url = product_url

    def product_info(self):
        response = requests.get(self.product_url)
        ld_json = get_ld_json(response)
        data = parse_json(ld_json)
        return data

    def product_reviews(self):
        ...

