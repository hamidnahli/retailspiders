import requests
import json
from typing import List, Dict
from items.utils import get_ld_json, parse_bazaarvoice_reviews
from datetime import datetime
from items.proxy import make_request
from items.debugging import app_logger as log

class Rei:
    product_info = None
    product_reviews = None
    product_sku = None

    def __init__(self, product_url, product_name = None, product_sku = None, session = None):
        if product_url.endswith('/'):
            self.product_url = product_url[:-1]
        else:
            self.product_url = product_url

        self.product_name = product_name
        self.product_sku = product_sku
        self.session = session


    @staticmethod
    def _parse_json(ld: json):
        '''
            {
            "@context":"https://schema.org",
            "@type":"Product",
            "@id":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
            "name":"Pranayama Wrap - Women's",
            "image":"https://www.rei.com/media/product/195355",
            "description":"Here's something you can wear to and from the studio, and every day for life off the mat. The women's Athleta Pranayama wrap layers easily over sports bras, tank tops, crop tops and yoga tees.",
            "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
            "sku":"195355",
            "category":"Women's Yoga Shirts",
            "weight":"Unavailable",
            "color":[
                "Black",
                "Bright White",
                "Marl Grey Heather",
                "Tawny Rose"
            ],
            "brand":{
                "@type":"Brand",
                "name":"Athleta",
                "url":"https://www.rei.com/b/athleta"
            },
            "offers":[
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550003",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550003",
                    "price":"61.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550014",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550014",
                    "price":"61.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550002",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550002",
                    "price":"61.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550013",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550013",
                    "price":"61.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550005",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550005",
                    "price":"61.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550016",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550016",
                    "price":"89.00",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550004",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550004",
                    "price":"61.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550015",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550015",
                    "price":"61.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550007",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550007",
                    "price":"65.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/OutOfStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550018",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550018",
                    "price":"89.00",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550006",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550006",
                    "price":"65.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550017",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550017",
                    "price":"89.00",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550009",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550009",
                    "price":"65.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/OutOfStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550008",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550008",
                    "price":"65.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/OutOfStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550019",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550019",
                    "price":"89.00",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550010",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550010",
                    "price":"65.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/OutOfStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550020",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550020",
                    "price":"89.00",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550001",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550001",
                    "price":"61.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550012",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550012",
                    "price":"61.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                },
                {
                    "@type":"Offer",
                    "image":"https://www.rei.com/media/product/1953550011",
                    "url":"https://www.rei.com/product/195355/athleta-pranayama-wrap-womens",
                    "priceValidUntil":"2022-06-28",
                    "sku":"1953550011",
                    "price":"61.93",
                    "priceCurrency":"USD",
                    "availability":"https://schema.org/InStock",
                    "itemCondition":"https://schema.org/NewCondition",
                    "availableDeliveryMethod":[
                        "https://schema.org/ParcelService"
                    ],
                    "seller":{
                        "@type":"Organization",
                        "name":"REI Co-op"
                    }
                }
            ],
            "aggregateRating":{
                "@type":"AggregateRating",
                "ratingValue":"5.0",
                "reviewCount":"18"
            },
            "gtin13":[
                "0135269600033",
                "0178228600040",
                "0135269600026",
                "0178228600033",
                "0135269600057",
                "0500074227384",
                "0135269600040",
                "0178228600057",
                "0136302200029",
                "0500074227407",
                "0136302200012",
                "0500074227391",
                "0136302200043",
                "0136302200036",
                "0500074227414",
                "0136302200050",
                "0500074227421",
                "0135269600019",
                "0178228600026",
                "0178228600019"
            ]
            }
        '''
        return {
            'sku' : ld.get('sku'),
            'title' : ld['name'],
            'description' : ld.get('description'),
            'price' : float(ld['offers'][0]['price']),
            'currency' : ld['offers'][0]['priceCurrency'],
            'brand' : ld['brand']['name'],
            'seller':ld['offers'][0]['seller']['name'],
            'image' : ld['image'],
            'category' : ld['category'],
            'review_count': ld['aggregateRating']['reviewCount'],
            'review_rating': ld['aggregateRating']['ratingValue'],
            'created': str(datetime.now()),
            'last_updated': str(datetime.now())
        }
    
    
    def get_product_info(self) -> Dict:
        if self.session:
            response = self.session.get(self.product_url)
        else:
            response = requests.get(self.product_url)
            
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)

        # Updating the product info dictionary
        data['product_url'] = self.product_url
        data['spider'] = Rei.__name__.lower()
        self.product_info = data
        self.product_sku = data['sku']
        log.info(f'{data["sku"]}, url: {self.product_url} - scrapped successfully')
        return data


    def get_product_review(self, proxy=False) -> List:
        
        if not self.product_info:
            if proxy:
                self.product_info = self.get_product_info(proxy=True)
            else:
                self.product_info = self.get_product_info()
                
        reviews = parse_bazaarvoice_reviews(self,self.product_sku)
        self.product_reviews = reviews
        return reviews

    