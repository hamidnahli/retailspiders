from numpy import product
import requests
import json
from typing import List, Dict
from dotenv import load_dotenv
from items.utils import get_ld_json,parse_yotpo_reviews
from bs4 import BeautifulSoup
import os
load_dotenv()


class Glossier:
    product_info = None

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
        
        return {
            # ADD AVAILABILITY
            'title': ld['name'],
            'description': ld.get('briefDescription'),
            'price': ld['offers']['price'],
            'currency': ld['offers']['priceCurrency'],
            'offer_item': ld['offers']['itemCondition'],
            'id': ld['@id'],
            'availability': ld['offers']['availability'],
            'brand': ld['brand']['name'],
            'image': ld['image'],
        }

    def get_product_info(self, proxy=False) -> Dict:
        response = requests.get(self.product_url)
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)
        # Updating the product info dictionary
        data['url'] = self.product_url
        data['spider'] = Glossier.__name__.lower()
        data['product_id'] = self.product_id
        self.product_info = data
        # variants = self.get_shopify_variants(response)
        return data
    
    # need to be fixed
    def get_shopify_variants(self):
        url='https://www.glossier.com/products/lidstar'
        response=requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        scripts=soup.find_all("script", {"type": "text/javascript"})[1].text
        scripts=scripts.replace('window.__routeInfo = JSON.parse("','')[:-3].replace('\\','')
        script = json.loads(scripts)
        print(type(script))
        return scripts
    
    def get_product_review(self):
        product_reviews = parse_yotpo_reviews()
        return product_reviews

    