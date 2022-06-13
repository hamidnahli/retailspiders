import json
import requests
from bs4 import BeautifulSoup


class Ulta:
    api_key = ""
    product_info = None
    product_reviews = None

    def __init__(self, url: str = None):
        self.url = url
        if url:
            self.product_info = self.scrap_product_info(self.url)
            self.product_reviews = self.scrap_reviews(self.url)

    # parse the ld+json that contain product information from teh html source page
    def parse_ld_json(self, soup):
        ld_json = soup.findAll('script', {'type': 'application/ld+json'})
        ld_json = [json.loads(ld.text) for ld in ld_json if 'product' in ld.text.lower()]
        if len(ld_json) != 0:
            ld_json = ld_json[0]
        else:
            ld_json = None
        return ld_json

    def parse_review(self, rev, url):
        review_keys = ['comments', 'headline', 'brand_base_url', 'brand_name', 'nickname', 'source', 'location',
                       'created_date', 'updated_date', 'bottom_line', 'product_page_id']
        metric_keys = ['helpful_votes', 'not_helpful_votes', 'rating', 'helpful_score']
        parsed_review = dict()
        parsed_review['product_url'] = url
        review = rev['details']
        metrics = rev['metrics']
        for key in review_keys:
            parsed_review[key] = review.get(key)
        for key in metric_keys:
            parsed_review[key] = metrics.get(key)
        return parsed_review

    def check_review(self, ld_json):
        if ld_json.get('aggregateRating'):
            product_rating_value = ld_json['aggregateRating']['ratingValue']
            product_review_count = ld_json['aggregateRating']['reviewCount']
        else:
            product_rating_value = None
            product_review_count = None
        return product_rating_value, product_review_count

    def scrap_product_info(self, url):
        product = None
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            ld_json = self.parse_ld_json(soup)
            if ld_json:
                product_id = ld_json['productID']
                product_name = ld_json['name']
                product_description = ld_json['description']
                product_brand = ld_json['brand']
                price = ld_json['offers']['price']
                product_rating_value, product_review_count = self.check_review(ld_json)
                product_image = ld_json['image']
                product = {
                    'product_id': product_id,
                    'product_name': product_name,
                    'product_description': product_description,
                    'product_brand': product_brand,
                    'price': price,
                    'product_rating_value': product_rating_value,
                    'product_review_count': product_review_count,
                    'product_image': product_image,
                }
            else:
                print('No ld_json found, contact us or check if there is an ld_json in the html page source code')
        elif str(response.status_code)[:2] == '40':
            print('url not found')
        return product

    def scrap_reviews(self, url):
        reviews = []
        pimprod = url.split('-')[-1]
        api_url = f'https://display.powerreviews.com/m/6406/l/en_US/product/{pimprod}/reviews?paging.from=0&paging.size=25&filters=&search=&sort=Newest&image_only=false&_noconfig=true&apikey={self.api_key}'
        response = requests.get(api_url)
        data = response.json()
        pages_total = data['paging']['pages_total']
        if pages_total > 1:
            next_from = 0
            for _ in range(pages_total):
                next_page = f'https://display.powerreviews.com/m/6406/l/en_US/product/{pimprod}/reviews?paging.from={next_from}&paging.size=20&filters=&search=&sort=Newest&image_only=false&_noconfig=true&apikey={self.api_key}'
                response = requests.get(next_page)
                data = response.json()
                reviews_list = data['results'][0]['reviews']
                for review in reviews_list:
                    reviews.append(self.parse_review(review, url))
                next_from += 25
        else:
            reviews_list = data['results'][0]['reviews']
            for review in reviews_list:
                reviews.append(self.parse_review(review, url))
        return reviews
