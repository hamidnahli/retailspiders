import requests
import json
from typing import List, Dict
from dotenv import load_dotenv
from items.utils import get_ld_json, global_headers
load_dotenv()

class   Asos:
    product_info = None
    product_variant = None
    product_reviews = None

    def __init__(self, product_url, product_name=None, product_sku=None, product_id=None, rtype=None):
        if product_url.endswith('/'):
            self.product_url = product_url[:-1]
        elif 'pr_prod_strat' in product_url:
            self.product_url = product_url.split('?')[0]
        else:
            self.product_url = product_url
        self.product_name = product_name
        self.product_sku = product_sku
        self.product_id = product_id
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
            'product_id' : ld['productID'],
            'product_url' : ld['url'],
        }

    def get_product_info(self, proxy=False) -> Dict:
        response = requests.get(self.product_url, headers=global_headers())
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)

        # Updating the product info dictionary
        data['product_url'] = self.product_url
        data['spider'] = Asos.__name__.lower()
        self.product_info = data
        return data
        
    def get_product_review(self):
        reviews = []
        self.product_info = self.get_product_info()
        product_id = self.product_info['product_id']

        url = f'https://www.asos.com/api/product/reviews/v1/products/{product_id}?offset=1&limit=100&include=Products&store=US&lang=en-US&filteredStats=reviews&sort=SubmissionTime:desc'
        response = requests.get(url)
        data = response.json()
        totalResults = data['totalResults']
        
        for offset in range(1,int(totalResults),100):
            url = f'https://www.asos.com/api/product/reviews/v1/products/{product_id}?offset={offset}&limit=100&include=Products&store=US&lang=en-US&filteredStats=reviews&sort=SubmissionTime:desc'
            response = requests.get(url)
            data = response.json()

            for ele in data['results']:
                if ele['reviewText']:
                    review_date = ele['submissionTime']
                    review_author = ele['userNickname']
                    review_location = ele['contentLocale']
                    review_header = ele['title']
                    review_body = ele['reviewText']
                    
                    review = {
                        'date': review_date,
                        'author': review_author,
                        'location': review_location,
                        'header': review_header,
                        'body': review_body,
                        #'thumbs_up': review_thumbs_up,
                        #'thumbs_down': review_thumbs_down,
                    }
                    reviews.append(review)
        return reviews
        