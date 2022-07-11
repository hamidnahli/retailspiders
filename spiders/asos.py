import requests
import json
from typing import List, Dict
from dotenv import load_dotenv
from items.utils import get_ld_json, global_headers, parse_api_reviews
load_dotenv()
from datetime import datetime

class   Asos:
    product_info = None
    product_review = None

    def __init__(self, product_url, product_name=None, product_sku=None, product_id=None):
        if product_url.endswith('/'):
            self.product_url = product_url[:-1]

        elif 'prd' in product_url:
            self.product_url = product_url.split('?')[0]
            
        else:
            self.product_url = product_url
        self.product_name = product_name
        self.product_sku = product_sku
        self.product_id = product_id

    @staticmethod
    def _parse_json(ld: json):
        '''
            {
                '@context': 'https://schema.org/', 
                '@type': 'Product', 
                'name': 'adidas Originals Ozrah trainers in pale nude', 
                'sku': '109868766', 
                'color': 'Beige', 
                'image': 'https://images.asos-media.com/products/adidas-originals-ozrah-trainers-in-pale-nude/201136102-1-beige', 
                'brand': {
                    '@type': 'Brand', 
                    'name': 'adidas Originals'}, 
                'description': 'Trainers by adidas Made for unboxing Low-profile design Pull tab for easy entry Lace-up fastening Padded tongue and cuff Signature adidas branding Adiprene cushioning for added comfort Durable rubber outsole Textured grip tread', 
                'productID': 201136102, 
                'url': 'https://www.asos.com/adidas-originals/adidas-originals-ozrah-trainers-in-pale-nude/prd/201136102', 
                'offers': {}
            }
        '''
        return {
            'title' : ld['name'],
            'sku' : ld['sku'],
            'description' : ld.get('description'),
            'image' : ld['image'],
            'url' : ld['url'],
            'brand' : ld['brand']['name'],
            'product_id' : ld['productID'],
            'product_url' : ld['url'],
            'created': str(datetime.now()),
            'last_updated': str(datetime.now())
        }

    def get_product_info(self, proxy=False) -> Dict:
        response = requests.get(self.product_url, headers=global_headers())
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)

        # Updating the product info dictionary
        data['product_url'] = self.product_url
        data['spider'] = Asos.__name__.lower()
        self.product_info = data
        self.product_id = self.product_info['product_id']
        return data
        
    def get_product_review(self):
        if self.product_id:
            product_review = parse_api_reviews(self)
        else:
            self.product_info = self.get_product_info()
            product_review = parse_api_reviews(self)

        return product_review
        