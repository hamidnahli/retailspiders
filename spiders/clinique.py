import requests
import json
from typing import List, Dict
from dotenv import load_dotenv
from items.utils import get_ld_json
from bs4 import BeautifulSoup


load_dotenv()

class Clinique:
    product_info = None
    product_reviews = None

    def __init__(self, product_url, product_name=None, product_sku=None, product_id=None):
        if product_url.endswith('/'):
            self.product_url = product_url[:-1]
        elif 'pr_prod_strat' in product_url:
            self.product_url = product_url.split('?')[0]
        else:
         self.product_url = product_url
        self.product_name = product_name
        self.product_sku = product_sku
        self.product_id = product_id
        
    @staticmethod
    def _parse_json(ld: json) -> Dict:
        if ld.get('aggregateRating'):
            ratingCount = ld.get('aggregateRating').get('ratingCount')
            ratingValue = ld.get('aggregateRating').get('ratingValue')
        else:
            ratingCount = None
            ratingValue = None
        """
        {
          "url":"https://www.clinique.com/product/4034/87057/skincare/serum/clinique-smart-clinical-repairtm-wrinkle-correcting-serum",
          "sku":"V17E01",
          "title":"Clinique Smart Clinical Repair™ Wrinkle Correcting Serum",
          "description":"A laser-focused clinical serum that targets wrinkles from multiple angles.",
          "ratingValue":4.2,
          "ratingCount ":"None",
          "seller_name":"Clinique",
          "seller_type":"Organization",
          "offer_image":"https://www.clinique.com/media/export/cms/products/181x209/clq_V17F01_181x209.png",
          "priceCurrency":"USD",
          "price":171,
          "availability":"http://schema.org/InStock",
          "offer_price":69,
          "brand":{
              "@type":"Brand",
              "name":"Clinique",
              "image":"https://www.clinique.com/media/export/cms/site-logo-2018_v2.png",
              "url":"https://www.clinique.com/"
          },
          "brand_name":"https://www.clinique.com/media/export/cms/site-logo-2018_v2.png",
          "brand_url":"https://www.clinique.com/",
          "image":"https://www.clinique.com/media/export/cms/products/1200x1500/cl_sku_V17E01_1200x1500_0.png",
          "product_url":"https://www.clinique.com/product/4034/87057/skincare/serum/clinique-smart-clinical-repairtm-wrinkle-correcting-serum?size=1.7_oz._%2F_50_ml"
        }
        
        """
        return {
          #ADD AVAILABILITY  
            'sku': ld['sku'],
            'title': ld['name'],
            'description': ld.get('description'),
            'ratingValue': ratingValue,
            'ratingCount ': ratingCount,
            'seller' : ld['offers'][0]['seller']['name'],
            'currency': ld['offers'][1]['priceCurrency'],
            'price': ld['offers'][1]['price'],
            'availability': ld['offers'][1]['availability'],
            'brand': ld['brand'],
            'image': ld['image'],
            'category': None,
        }
    def get_product_info(self, proxy=False) -> Dict:
        response = requests.get(self.product_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.product_id = soup.find('meta',{"name":"productId"}).get('content')
        ld_json = get_ld_json(response)
        data = self._parse_json(ld_json)
        
        # Updating the product info dictionary
        data['product_url'] = self.product_url
        data['spider'] = Clinique.__name__.lower()
        data['product_id'] = self.product_id
        self.product_info = data
        return data

    def get_product_review(self):
        reviews = []
        product_id = self.product_id
        
        url = f'https://display.powerreviews.com/m/166973/l/en_US/product/{product_id}/reviews?paging.from=1&paging.size=25&filters=&search=&sort=Newest&image_only=false&page_locale=en_US&_noconfig=true&apikey=528023b7-ebfb-4f03-8fee-2282777437a7'
        response = requests.get(url)
        data = response.json()
        pages_total=data['paging']['total_results']
        
        for paging_from in range(1, pages_total, 25):
            
            url = f'https://display.powerreviews.com/m/166973/l/en_US/product/{product_id}/reviews?paging.from={paging_from}&paging.size=25&filters=&search=&sort=Newest&image_only=false&page_locale=en_US&_noconfig=true&apikey=528023b7-ebfb-4f03-8fee-2282777437a7'
            response = requests.get(url)
            data = response.json()
            
            for ele in data['results'][0]['reviews']:
                
                review_comment = ele['details']['comments']
                review_headline = ele['details']['headline']
                review_location = ele['details']['location']
                review_date = ele['details']['created_date']
                review_author = ele['details']['nickname']
                review_thumbs_up = ele['metrics']['helpful_votes']
                review_thumbs_down = ele['metrics']['not_helpful_votes']
                

                review = {
                            'date': review_date,
                            'author': review_author ,
                            'location': review_location,
                            'header': review_headline,
                            'body': review_comment,
                            'thumbs_up': review_thumbs_up,
                            'thumbs_down': review_thumbs_down,
                            'pages_total':pages_total
                        }
         
                reviews.append(review)
        reviews = json.dumps(reviews, indent = 4)
        with open("reviews.json", "w") as outfile:
            outfile.write(reviews)
            
        return reviews
      
        
     
