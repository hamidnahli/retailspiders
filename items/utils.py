import json
import os
import requests
from typing import Any, Dict, List

from dotenv import load_dotenv
from bs4 import BeautifulSoup

from items.debugging import app_logger as log

load_dotenv()

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

def parse_bazaarvoice_reviews(self):
    product_reviews = []
    product_id = self.product_sku

    def _get_data_totolresult(product_id,offset=0):
        api_rei_key = os.getenv('api_rei_key')
        url = f'https://api.bazaarvoice.com/data/batch.json?passkey={api_rei_key}&apiversion=5.5&displaycode=15372-en_us&resource.q0=reviews&filter.q0=isratingsonly%3Aeq%3Afalse&filter.q0=productid%3Aeq%3A{product_id}&filter.q0=contentlocale%3Aeq%3Aen*%2Cen_US&sort.q0=submissiontime%3Adesc&stats.q0=reviews&filteredstats.q0=reviews&include.q0=authors%2Cproducts%2Ccomments&filter_reviews.q0=contentlocale%3Aeq%3Aen*%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen*%2Cen_US&filter_comments.q0=contentlocale%3Aeq%3Aen*%2Cen_US&limit.q0=100&offset.q0={offset}&limit_comments.q0=20&callback=bv_351_1793'
        response = requests.get(url).text
        data = response.replace('bv_351_1793(','')[:-1]
        data = json.loads(data)
        totalResults = data['BatchedResults']['q0']['TotalResults']
        return [data,totalResults]

    totalResults = _get_data_totolresult(product_id,offset=0)[1]

    for offset in range(0,totalResults,100): 
        data = _get_data_totolresult(product_id,offset)[0]

        for ele in data['BatchedResults']['q0']['Results']:
            review_date = ele['SubmissionTime']
            review_author = ele['UserNickname']
            review_location = ele['UserLocation']
            review_header = ele['Title']
            review_body = ele['ReviewText']
            review_thumbs_up = ele['TotalPositiveFeedbackCount']
            review_thumbs_down = ele['TotalNegativeFeedbackCount']

            review = {
                    'date': review_date,
                    'author': review_author,
                    'location': review_location,
                    'header': review_header,
                    'body': review_body,
                    'thumbs_up': review_thumbs_up,
                    'thumbs_down': review_thumbs_down
                }
            product_reviews.append(review)      
    
    return product_reviews
