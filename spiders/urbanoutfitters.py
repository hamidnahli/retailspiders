import requests
import json
from typing import List, Dict

from dotenv import load_dotenv

from items.utils import get_ld_json, get_shopify_variants, global_headers, parse_stamped_reviews

load_dotenv()

class Urbanoutfitters:
    product_info = None
    product_variant = None
    product_reviews = None
 
    def __init__(self, product_url, product_name=None, product_sku=None, rid=None):
        if product_url.endswith('/'):
            self.product_url = product_url[:-1]
        elif 'pr_prod_strat' in product_url:
            self.product_url = product_url.split('?')[0]
        else:
            self.product_url = product_url
        self.product_name = product_name
        self.product_sku = product_sku
        self.rid = rid

    @staticmethod
    def _parse_json(ld: json):
        '''
        {
            "@context":"https://schema.org",
            "@type":"Product",
            "name":"Reebok LT Court Sneaker",
            "image":[
                "https://images.urbndata.com/is/image/UrbanOutfitters/64307614_011_b?$xlarge$&fit=constrain&qlt=80&wid=640",
                "https://images.urbndata.com/is/image/UrbanOutfitters/64307614_011_d?$xlarge$&fit=constrain&qlt=80&wid=640",
                "https://images.urbndata.com/is/image/UrbanOutfitters/64307614_011_e?$xlarge$&fit=constrain&qlt=80&wid=640",
                "https://images.urbndata.com/is/image/UrbanOutfitters/64307614_011_f?$xlarge$&fit=constrain&qlt=80&wid=640"
            ],
            "description":"It looks and feels like these LT Court shoes were pulled from the '80s Reebok archives. A rich garment leather upper that feels buttery soft, a luxe suede toe cap and heel tab, and a soft terry lining all stay true to OG style. Hits of color add just enough pop. A TPU accent piece seals the deal.\n\n**Content + Care**  \n\\- Leather, suede, EVA, rubber  \n\\- Spot clean  \n\\- Imported\n\n**Size + Fit**  \n\\- True to size",
            "mpn":"64307614",
            "sku":"64307614",
            "category":"Women's > Shoes",
            "brand":{
                "@type":"Thing",
                "name":"Reebok"
            },
            "offers":{
                "@type":"AggregateOffer",
                "offerCount":0,
                "highPrice":100,
                "lowPrice":100,
                "priceCurrency":"USD",
                "itemCondition":"https://schema.org/NewCondition",
                "seller":{
                    "@type":"Organization",
                    "name":"Urban Outfitters"
                },
                "offers":[
                    
                ]
            },
            "aggregateRating":{
                "@type":"AggregateRating",
                "ratingCount":8,
                "ratingValue":1.875
            }
            }
        '''
        return {
            'title' : ld['name'],
            'description' : ld.get('description'),
            'brand' : ld['brand']['name'],
            'price' : ld['offers']['lowPrice'],
            'seller' : ld['offers']['seller']['name'],
            'category' : ld['category'],
            'image' : ld['image'],
            'Currency' : ld['offers']['priceCurrency'],
            'sku' : ld['sku'],
            'ratingCount': ld['aggregateRating']['ratingCount'],
            'ratingValue': ld['aggregateRating']['ratingValue'],
        }

    def get_product_info(self, proxy=False) -> Dict:
        response = requests.get(self.product_url,headers=global_headers())
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)

        # rid and rtype will be used later for scraping reviews.
        #self.rid, self.rtype, self.product_variant = get_shopify_variants(response)

        # Updating the product info dictionary
        data['product_url'] = self.product_url
        data['spider'] = Urbanoutfitters.__name__.lower()
        data['rid'] = self.rid
        self.product_info = data
        return data

    def get_product_review(self) -> List:
        reviews = []
        
        pass

