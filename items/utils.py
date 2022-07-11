import json
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from items.debugging import app_logger as log
load_dotenv()

def global_headers():
    return {
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,de;q=0.6',
            }

def get_ld_json(response: requests.Response):
    soup = BeautifulSoup(response.content, 'html.parser')
    lds = soup.findAll('script', {'type': 'application/ld+json'})
    if lds:
        for ld in lds:
            if "Product" in ld.text:
                return json.loads(ld.text)
    else:
        log.info(f'ld+json not found for {response.url}')
    return None

def parse_api_reviews(self):
    product_id = self.product_id
    reviews = []
    def _get_totalResults(product_id):
        url = f'https://www.asos.com/api/product/reviews/v1/products/{product_id}?offset=1&limit=100&include=Products&store=US&lang=en-US&filteredStats=reviews&sort=SubmissionTime:desc'
        response = requests.get(url)
        data = response.json()
        totalResults = data['totalResults']
        return totalResults
        
    for offset in range(1,int(_get_totalResults(product_id)),100):
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
                }
                reviews.append(review)
    return reviews