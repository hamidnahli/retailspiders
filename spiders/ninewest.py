import requests
import json
from typing import List, Dict

from dotenv import load_dotenv

from items.utils import get_ld_json, get_shopify_variants


load_dotenv()


class NineWest:
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
    def _parse_json(ld: json) -> Dict:
        """
        URL: https://ninewest.com/products/speakup-almond-toe-flats-in-tortoise
        {
          "@context": "http://schema.org/",
          "@type": "Product",
          "name": "Speakup Almond Toe Flats",
          "image": "https:\/\/cdn.shopify.com\/s\/files\/1\/0267\/3737\/7324\/products\/PG.WNSPEAKUP3-DBR01.RZ_1024x1024.jpg?v=1620412028",
          "description": "Best seller. Stay on point with the classic, trend-right style of our Speakup flats. This flattering, wear-with-anything almond-toe design is destined to be one of your go-to shoes this season.",
          "brand": {
            "@type": "Thing",
            "name": "Nine West"
          },
          "sku": "195972397897",
          "mpn": "195972397897",
          "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "price": 39.6,
            "availability": "http://schema.org/InStock",
            "url": "https://ninewest.com/products/speakup-almond-toe-flats-in-tortoise?variant=39365994676268",
            "seller": {
              "@type": "Organization",
              "name": "Nine West"
            },
            "priceValidUntil": "2023-06-20"
          }
        }
        """
        return {
            'sku': ld['sku'],
            'title': ld['name'],
            'description': ld['description'],
            'price': ld['offers']['price'],
            'currency': ld['offers']['priceCurrency'],
            'brand': ld['brand']['name'],
            'seller': ld['offers']['seller']['name'],
            'image': ld['image'],
            'category': None,
            'review_count': None,
            'review_rating': None
        }

    def get_product_info(self, proxy=False) -> Dict:
        response = requests.get(self.product_url)
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)

        # Assigning initial variables for later use.
        self.product_name = '+'.join(list(data['title']))
        self.product_sku = self.product_url.split('/')[-1]

        # rid and rtype will be used later for scraping reviews.
        self.rid, self.rtype, self.product_variant = get_shopify_variants(response)

        # Updating the product info dictionary
        data['product_url'] = self.product_url
        data['spider'] = NineWest.__name__.lower()
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
