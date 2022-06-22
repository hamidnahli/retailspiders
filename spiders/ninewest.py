import requests

from utils import get_ld_json, parse_json


class NineWest:

<<<<<<< Updated upstream
    def __init__(self, product_url):
        self.product_url = product_url
=======
    def __init__(self, product_url, product_name=None, product_sku=None, rid=None, rtype=None):

        if product_url.endswith('/'):
            self.product_url = product_url[:-1]

        elif 'pr_prod_strat' in product_url:
            self.product_url = product_url.split('?')[0]
            
        else:
            self.product_url = product_url
        self.product_name = product_name
        self.product_sku = product_sku
        self.rid = rid
        self.rtype = rtype
>>>>>>> Stashed changes

    def product_info(self):
        response = requests.get(self.product_url)
        ld_json = get_ld_json(response)
        data = parse_json(ld_json)
        return data
