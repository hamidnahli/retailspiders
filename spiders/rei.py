from h11 import Data
import requests
import json
from typing import List, Dict
from dotenv import load_dotenv
from items.utils import get_ld_json, get_shopify_variants, parse_stamped_reviews
from bs4 import BeautifulSoup

load_dotenv()

class Rei:
    product_info = None
    product_variant = None
    product_reviews = None

    def __init__(self, product_url, product_name=None, product_sku=None, rtype=None):
        if product_url.endswith('/'):
            self.product_url = product_url[:-1]
        elif 'pr_prod_strat' in product_url:
            self.product_url = product_url.split('?')[0]
        else:
            self.product_url = product_url
        self.product_name = product_name
        self.product_sku = product_sku
        self.rtype = rtype

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
            'title' : ld['name'],
            'description' : ld.get('description'),
            'brand' : ld['brand']['name'],
            'price' : ld['offers'][0]['price'],
            'image' : ld['image'],
            'currency' : ld['offers'][0]['priceCurrency'],
            'sku' : ld['sku'],
            'category' : ld['category'],
            'seller':ld['offers'][0]['seller']['name'],
            'review_count': ld['aggregateRating']['reviewCount'],
            'review_rating': ld['aggregateRating']['ratingValue'],
        }
    
    def get_product_info(self, proxy=False) -> Dict:
        response = requests.get(self.product_url)
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)

        # Updating the product info dictionary
        data['product_url'] = self.product_url
        data['spider'] = Rei.__name__.lower()
        self.product_info = data
        return data

    def get_product_review(self) -> List:
        reviews = []
        product_id = self.product_info['sku']

        def get_response(product_id,offset=0):
            url = f'https://api.bazaarvoice.com/data/batch.json?passkey=thvpbov9ywkkl4nkhbeq0wm1i&apiversion=5.5&displaycode=15372-en_us&resource.q0=reviews&filter.q0=isratingsonly%3Aeq%3Afalse&filter.q0=productid%3Aeq%3A{product_id}&filter.q0=contentlocale%3Aeq%3Aen*%2Cen_US&sort.q0=submissiontime%3Adesc&stats.q0=reviews&filteredstats.q0=reviews&include.q0=authors%2Cproducts%2Ccomments&filter_reviews.q0=contentlocale%3Aeq%3Aen*%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen*%2Cen_US&filter_comments.q0=contentlocale%3Aeq%3Aen*%2Cen_US&limit.q0=100&offset.q{offset}=0&limit_comments.q0=20&callback=bv_351_1793'
            response = requests.get(url).text
            data = response.replace('bv_351_1793(','')[:-1]
            data = json.loads(data)
            totalResults = data['BatchedResults']['q0']['TotalResults']
            return data, totalResults

        data, totalResults = get_response(product_id,offset=0)

        for offset in range(0,int(totalResults),10):

            data = get_response(product_id,offset=offset)

            review_date = data[0]['BatchedResults']['q0']['Results'][0]['SubmissionTime']
            review_author = data[0]['BatchedResults']['q0']['Results'][0]['UserNickname']
            review_location = data[0]['BatchedResults']['q0']['Results'][0]['UserLocation']
            review_header = data[0]['BatchedResults']['q0']['Results'][0]['Title']
            review_body = data[0]['BatchedResults']['q0']['Results'][0]['ReviewText']
            review_thumbs_up = data[0]['BatchedResults']['q0']['Results'][0]['TotalPositiveFeedbackCount']
            review_thumbs_down = data[0]['BatchedResults']['q0']['Results'][0]['TotalNegativeFeedbackCount']

            review = {
                    'date': review_date,
                    'author': review_author,
                    'location': review_location,
                    'header': review_header,
                    'body': review_body,
                    'thumbs_up': review_thumbs_up,
                    'thumbs_down': review_thumbs_down
                }
            reviews.append(review)


        return reviews
