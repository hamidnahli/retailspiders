import json
import requests

from datetime import datetime
from typing import Dict, List

from items.utils import get_ld_json
from items.debugging import app_logger as log

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

reviews_headers = {
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'x-latency-trace': '1',
    'WM_MP': 'true',
    'x-o-platform-version': 'main-1.5.1-fda6c9',
    'x-o-segment': 'oaoh',
    'x-o-gql-query': 'query ReviewsById',
    'X-APOLLO-OPERATION-NAME': 'ReviewsById',
    'sec-ch-ua-platform': '"macOS"',
    'x-o-bu': 'WALMART-US',
    'x-o-mart': 'B2C',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'x-o-platform': 'rweb',
    'Content-Type': 'application/json',
    'accept': 'application/json',
    'x-enable-server-timing': '1',
    'x-o-ccm': 'server',
}


class Walmart:
    product_info = None
    product_reviews = None
    product_variants = None

    def __init__(self, product_url, session=None):
        self.session = session
        if '?' in product_url:
            self.product_url = product_url.spli('?')[0]
        else:
            self.product_url = product_url

    def _parse_json(self, ld: json) -> Dict:
        """
            URL: https://www.walmart.com/ip/ASUS-CM3200-MKT-4-64-2-in-1-Chromebook-12-HD-Touch-MediaTek-8192-4GB-RAM-64GB-eMMC-Mineral-Gray-Chrome-OS-CM3200FM1A-WS44T/884666252
            {
              "@context": "https://schema.org",
              "@type": "Product",
              "image": "https://i5.walmartimages.com/asr/3e0c2a72-ec3e-4449-8c84-9c6c11288237.fa9ff342dd94ec8fda71a69dd53f452c.jpeg",
              "name": "ASUS CM3200 MKT 4/64 2-in-1 Chromebook, 12\" HD+ Touch, MediaTek 8192, 4GB RAM, 64GB eMMC, Mineral Gray, Chrome OS, CM3200FM1A-WS44T",
              "sku": "884666252",
              "gtin13": "195553595520",
              "description": "ASUS Chromebook Flip CM3 strikes the balance between work and play.  The 360 degree hinge enables multiple modes and provides the versatility to work or study using the orientation that you like best.  Featuring a 12-inch display with a 3:2 aspect ratio and thin bezels, the ASUS Chromebook Flip CM3 provides an expanded view in the portrait orientation to inspire you to see the world from a new perspective.  ASUS Pen USI stylus support enables intuitive writing with an active stylus for enhanced productivity.  The ultra-portable design and long-lasting battery life are tailored to an on-the-go lifestyle, and the silky-smooth palm rests and ErgoLift hinge design enusre comfort when typing.  With vast storage and a rich library of apps, the ASUS Chromebook Flip CM3 opens up a whole new world of freedom!",
              "model": "CM3200FM1A-WS44T",
              "brand": {
                "@type": "Thing",
                "name": "ASUS"
              },
              "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": 4.8,
                "bestRating": 5,
                "reviewCount": 37
              },
              "offers": {
                "@type": "Offer",
                "url": "https://www.walmart.com/ip/ASUS-CM3200-MKT-4-64-2-in-1-Chromebook-12-HD-Touch-MediaTek-8192-4GB-RAM-64GB-eMMC-Mineral-Gray-Chrome-OS-CM3200FM1A-WS44T/884666252",
                "priceCurrency": "USD",
                "price": 299,
                "availability": "https://schema.org/InStock",
                "itemCondition": "https://schema.org/NewCondition",
                "availableDeliveryMethod": "https://schema.org/OnSitePickup"
              }
            }
        """
        if ld.get('aggregateRating'):
            review_count = ld['aggregateRating']['reviewCount']
            review_rating = ld['aggregateRating']['ratingValue']
        else:
            review_count = None
            review_rating = None
        return {
            'sku': ld['sku'],
            'title': ld['name'],
            'description': ld.get('description'),
            'price': ld['offers']['price'],
            'currency': ld['offers']['priceCurrency'],
            'brand': ld['brand']['name'],
            'seller_id': None,
            'seller': None,
            'review_count': review_count,
            'review_rating': review_rating,
            'spider': type(self).__name__,
            'created': str(datetime.now()),
            'last_updated': str(datetime.now()),
            'image': ld['image'],
            'product_url': self.product_url
        }

    def get_product_info(self):
        if self.session:
            response = self.session.get(self.product_url, headers=headers)
        else:
            response = requests.get(self.product_url, headers=headers)
        ld_json = get_ld_json(response)
        self.product_info = self._parse_json(ld_json)
        # insert info to db
        log.info(f'product {self.product_info["sku"]} scrapped successfully')

    def get_product_reviews(self, page=1):
        if not self.product_info:
            self.get_product_info()
        body = {
            "query": "query ReviewsById( $itemId:String! $page:Int $sort:String $limit:Int $filters:[String]$lookup:String $aspect:Int ){reviews( itemId:$itemId page:$page limit:$limit sort:$sort filters:$filters lookupId:$lookup aspectId:$aspect ){activePage activeSort aspectId aspects{...aspectFragment}negativeCount positiveCount averageOverallRating customerReviews{...customerReviewsFragment}topPositiveReview{...customerReviewsFragment}topNegativeReview{...customerReviewsFragment}lookupId overallRatingRange percentageOneCount percentageTwoCount percentageThreeCount percentageFourCount percentageFiveCount ratingValueOneCount ratingValueTwoCount ratingValueThreeCount ratingValueFourCount ratingValueFiveCount recommendedPercentage roundedAverageOverallRating totalReviewCount aspectReviewsCount pagination{...paginationFragment}}product(itemId:$itemId){name canonicalUrl category{path{name url}}sellerId sellerName priceInfo{currentPrice{priceString}}}}fragment aspectFragment on Aspect{id name score snippetCount}fragment customerReviewsFragment on CustomerReview{authorId badges{badgeType contentType id glassBadge{id text}}userLocation negativeFeedback positiveFeedback rating recommended reviewId reviewSubmissionTime reviewText reviewTitle reviewAspectStart reviewAspectEnd reviewSentimentStart reviewSentimentEnd snippetFromTitle showRecommended syndicationSource{contentLink logoImageUrl name}userNickname externalSource photos{caption id sizes{normal{...reviewPhotoSizeFragment}thumbnail{...reviewPhotoSizeFragment}}}}fragment reviewPhotoSizeFragment on ReviewPhotoSize{id url}fragment paginationFragment on Pagination{currentSpan next{num url active gap}pages{num url active gap}previous{num url active gap}total}",
            "variables": {
                "itemId": self.product_info['sku'],
                "page": page,
                "sort": "relevancy",
                "limit": 20,
                "filters": [],
                "lookup": "",
                "aspect": 0
            }
        }
        response = self.session.post(
            'https://www.walmart.com/orchestra/home/graphql',
            json=body,
            headers=reviews_headers
        )
        data = response.json()
        self.update_product_info(data)
        # update the info in db
        customer_reviews = data['data']['reviews']['customerReviews']
        self.product_info = [self.product_info, *self.parse_reviews(customer_reviews)]
        pages = len(data['data']['reviews']['pagination']['pages'])
        if pages > 1:
            for _ in range(2, pages + 1):
                response = self.session.get(
                    url='https://www.walmart.com/orchestra/home/graphql',
                    headers=reviews_headers,
                    json=body
                )
                data = response.json()
                customer_reviews = data['data']['reviews']['customerReviews']
                self.product_info = [self.product_info, *self.parse_reviews(customer_reviews)]

    def parse_reviews(self, reviews: List) -> List:
        parsed_reviews = []
        review = {}
        for item in reviews:
            review['author_id'] = item['authorId']
            review['author'] = item['userNickname']
            review['location'] = item['userLocation']
            review['thumps_down'] = item['negativeFeedback']
            review['thumps_up'] = item['positiveFeedback']
            review['rating'] = item['rating']
            review['recommended'] = item['recommended']
            review['review_id'] = item['reviewId']
            review['review_date'] = item['reviewSubmissionTime']
            review['body'] = item['reviewText']
            review['header'] = item['reviewTitle']
            review['reviewAspectStart'] = item['reviewAspectStart']
            review['reviewAspectEnd'] = item['reviewAspectEnd']
            review['reviewSentimentStart'] = item['reviewSentimentStart']
            review['reviewSentimentEnd'] = item['reviewSentimentEnd']
            review['source'] = item['externalSource']
            review['product_sku'] = self.product_info['sku']
            parsed_reviews.append(review)
        return parsed_reviews

    def update_product_info(self, data: dict):
        print(data)
        self.product_info['overallRatingRange'] = data['data']['reviews'].get('overallRatingRange')
        self.product_info['percentageOneCount'] = data['data']['reviews'].get('percentageOneCount')
        self.product_info['percentageTwoCount'] = data['data']['reviews'].get('percentageTwoCount')
        self.product_info['percentageThreeCount'] = data['data']['reviews'].get('percentageThreeCount')
        self.product_info['percentageFourCount'] = data['data']['reviews'].get('percentageFourCount')
        self.product_info['percentageFiveCount'] = data['data']['reviews'].get('percentageFiveCount')
        self.product_info['ratingValueOneCount'] = data['data']['reviews'].get('ratingValueOneCount')
        self.product_info['ratingValueTwoCount'] = data['data']['reviews'].get('ratingValueTwoCount')
        self.product_info['ratingValueThreeCount'] = data['data']['reviews'].get('ratingValueThreeCount')
        self.product_info['ratingValueFourCount'] = data['data']['reviews'].get('ratingValueFourCount')
        self.product_info['ratingValueFiveCount'] = data['data']['reviews'].get('ratingValueFiveCount')

        self.product_info['sellerName'] = data['data']['product']['sellerName']
        self.product_info['sellerId'] = data['data']['product']['sellerId']

        category = data['data']['product']['category']['path']
        category = [ele['name'] for ele in category]
        self.product_info['category'] = category
