import requests
import json
from typing import List, Dict
from dotenv import load_dotenv
from items.utils import get_ld_json, get_shopify_variants, parse_stamped_reviews, global_headers

load_dotenv()

class   Asos:
    product_info = None
    product_variant = None
    product_reviews = None

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
            'rid' : ld['productID'],
            'product_url' : ld['url'],
        }

    def get_product_info(self, proxy=False) -> Dict:
        response = requests.get(self.product_url, headers=global_headers())
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)

        # Assigning initial variables for later use.
        self.product_name = '+'.join(list(data['title']))
        self.product_sku = self.product_url.split('/')[-1]

        # rid and rtype will be used later for scraping reviews.
        #self.rid, self.rtype, self.product_variant = get_shopify_variants(response)

        # Updating the product info dictionary
        data['product_url'] = self.product_url
        data['spider'] = Asos.__name__.lower()
        data['rtype'] = self.rtype
        self.product_info = data
        print(data['rid'])
        return ld_json
    
    def get_product_review(self) -> List:
        if not self.product_info:
            self.product_info = self.get_product_info()

        rating, count, reviews = parse_stamped_reviews(self.rid, self.rtype, self.product_name, self.product_sku)
        self.product_reviews = reviews
        self.product_info['review_count'] = count
        self.product_info['review_rating'] = rating
        return reviews