import requests
import json
from typing import List, Dict

from dotenv import load_dotenv

from items.utils import get_ld_json, get_shopify_variants, parse_stamped_reviews, global_headers

load_dotenv()

class   Anthropologie:
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
        URL: https://www.anthropologie.com/shop/facial-rounds?color=000&recommendation=home-hpg-tray-1-sfrectray-homepagetrendingmostpurchased&type=STANDARD&size=One%20Size&quantity=1
        {
            'name': 'Facial Rounds',
            'sku': '67874057', 
            'seller': 'Anthropologie', 
            'description': None, 
            'Currency': 'USD', 
            'image': 
                ['https://images.urbndata.com/is/image/Anthropologie/67874057_000_b?$a15-pdp-detail-shot$&fit=constrain&qlt=80&wid=640', 
                'https://images.urbndata.com/is/image/Anthropologie/67874057_000_b2?$a15-pdp-detail-shot$&fit=constrain&qlt=80&wid=640'], 
            'price': 12.8, 
            'category': 'SMART: Makeup', 
            'product_ratingCount': None, 
            'product_ratingValue': None}
        '''

        if ld.get('aggregateRating'):
            product_ratingCount = ld.get('aggregateRating').get('ratingCount')
            product_ratingValue = ld.get('aggregateRating').get('ratingValue')
        else :
            product_ratingCount = None
            product_ratingValue = None
        return {
            'title' : ld['name'],
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

    def get_product_info(self, proxy=False) -> Dict:
        response = requests.get(self.product_url, headers=global_headers())
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)

        # Assigning initial variables for later use.
        self.product_name = '+'.join(list(data['title']))
        self.product_sku = self.product_url.split('/')[-1]

        # rid and rtype will be used later for scraping reviews.
        self.rid, self.rtype, self.product_variant = get_shopify_variants(response)

        # Updating the product info dictionary
        data['product_url'] = self.product_url
        data['spider'] = Anthropologie.__name__.lower()
        data['rid'] = self.rid
        data['rtype'] = self.rtype
        self.product_info = data
        return data

    def get_product_review(self) -> List:
        if not self.product_info:
            self.product_info = self.get_product_info()

        rating, count, reviews = parse_stamped_reviews(self.rid, self.rtype, self.product_name, self.product_sku)
        self.product_reviews = reviews
        self.product_info['review_count'] = count
        self.product_info['review_rating'] = rating
        return reviews
    
