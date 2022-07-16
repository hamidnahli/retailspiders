import datetime
import requests
import json
from typing import Dict
from dotenv import load_dotenv
from items.utils import get_ld_json, parse_yotop_reviews
from bs4 import BeautifulSoup
load_dotenv()

class Glossier:
    product_info = None
    product_reviews = None
    product_variants = None
    
    def __init__(self, product_url, product_name=None, product_sku=None, product_id=None):
        if product_url.endswith('/'):
            self.product_url = product_url[:-1]
        elif 'pr_prod_strat' in product_url:
            self.product_url = product_url.split('?')[0]
        else:
            self.product_url = product_url
        self.product_name = product_name
        self.product_sku = product_sku
        self.product_id = product_id
    
    @staticmethod
    def _parse_json(ld: json) -> Dict:
        """
        {
          '@context': 'http://schema.org',
          '@type': 'Product',
          '@id': 'lidstar',
          'name': 'Lidstar',
          'image': 'https://static-assets.glossier.com/production/spree/images/attachments/000/003/757/portrait_normal/Lidstar.jpg?1556563486',
          'briefDescription': None, 'url': 'https://www.glossier.com/products/lidstar',
          'brand':
          {
              '@type': 'Brand',
              'name':'Glossier'
              },
              'offers':
              {
                  '@type': 'Offer',
                  'price': '18.0',
                  'priceCurrency': 'USD',
                  'itemCondition': 'new',
                  'availability': 'InStock'}
                  }
        """
        return {
            # ADD AVAILABILITY
            'title': ld['name'],
            'description': ld.get('briefDescription'),
            'price': ld['offers']['price'],
            'currency': ld['offers']['priceCurrency'],
            # 'offer_item': ld['offers']['itemCondition'],
            # 'availability': ld['offers']['availability'],
            'brand': ld['brand']['name'],
            'seller': None,
            'image': ld['image'],
            'category': None,
            'review_count': None,
            'review_rating':None,
            'created': str(datetime.datetime.now()),
            'last_updated': str(datetime.datetime.now())
        }
    
    def get_product_info(self, proxy=False) -> Dict:
        response = requests.get(self.product_url)
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)
        # Updating the product info dictionary
        data['url'] = self.product_url
        data['spider'] = type(self).__name__
        # data['product_id'] = self.product_id
        self.product_info = data
        # variants = self.get_shopify_variants(response)
        return data

    def get_product_review(self):
        if not self.product_info:
            self.product_info = self.get_product_info()
        product_reviews = parse_yotop_reviews()
        
        return product_reviews