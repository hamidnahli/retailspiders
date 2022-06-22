from urllib.parse import urlparse
import requests

from items import utils

BASE_URL = ''
class Sephora:
    api_key = ""
    BASE_URL = 'https://www.sephora.com'
    product_info = []
    product_reviews = []
    productid = None

    def __init__(self, url, productid: str = None):
        self.url = url
        self.productid = productid
        if url:
            self.productid = self.extract_product_id(self.url)

    def extract_product_id(self, url):
        product_path = urlparse(url).path
        product_id = product_path.split('-')[-1]
        if product_id.startswith('P'):
            product_id = product_id
        else:
            print(f'Invalid product url: {url}\nPlease contact  us on github if the url renders product details.')
        return product_id

    def parse_product_info(self, productid):
        url = f'https://api.bazaarvoice.com/data/reviews.json?Filter=contentlocale%3Aen*&Filter=ProductId%3A{productid}&Sort=SubmissionTime%3Adesc&Limit=24&Offset=24&Include=Products%2CComments&Stats=Reviews&passkey={self.api_key}&apiversion=5.4&Locale=en_US '
        response = requests.get(url)
        data = response.json()
        # Check if there are any product returns
        if data.get('Includes'):
            products = data['Includes']['Products']
            product_keys = list(products.keys())
            for key in product_keys:
                product = {key: products[key]}
                self.product_info.append(product)
        else:
            print('No product found, please check url or the product ID')

    def scrap_product_info(self):
        if isinstance(self.productid, str):
            self.parse_product_info(self.productid)

    def parse_product_reviews(self, productid):
        url = f'https://api.bazaarvoice.com/data/reviews.json?Filter=contentlocale%3Aen*&Filter=ProductId%3A{productid}&Sort=SubmissionTime%3Adesc&Limit=24&Offset=24&Include=Products%2CComments&Stats=Reviews&passkey={self.api_key}&apiversion=5.4&Locale=en_US '
        urls = []
        response = requests.get(url)
        data = response.json()
        pages = round(data['TotalResults']) + 1
        reviews = data['Results']
        self.product_reviews = self.product_reviews + reviews
        next_url = utils.get_next_url(url, 'Offset', 24)
        if len(reviews) != 0:
            # Scrap the remaining reviews
            while len(data['Results']) != 0:
                response = requests.get(next_url)
                data = response.json()
                reviews = data['Results']
                self.product_reviews = self.product_reviews + reviews
                next_url = utils.get_next_url(next_url, 'Offset', 24)
        return reviews

    def scrap_product_reviews(self):
        if isinstance(self.productid, str):
            self.parse_product_reviews(self.productid)
