# Ecommerce Retailer Scraper

The purpose of this project is to create a library of spiders/scraper for major online ecommerce retailer shop such as Amazon, Sephora, Walmart, and many other brands. The app will return product information and review as well in JSON format. 

The extracted data you can use for market research, product design, consumer buying impulse...The sky is the limit.

## Instruction:
1. How to install:
```bash
pip install ecom-scraper
```
2. How to use:

```python
from spiders import Sephora

# Sephora spider take either product url or productid Sephora(url=url, productid=product_id)
url = 'https://www.sephora.com/product/huda-beauty-liquid-matte-ultra-comfort-transfer-proof-lipstick-P479843'
product_id = 'P479843'
sephora = Sephora(url=url)
# Or
sephora = Sephora(productid=product_id)
sephora.scrap_product_info()  # Instantiate the Scrap product function
info = sephora.product_info  # product info and its variants will be stored in product_info
sephora.scrap_product_reviews()  # Instantiate The Scrap product reviews function
reviews = sephora.product_reviews  # All product reviews will be stored in product_reviews
```
## Supported Scrapers


- [Ulta Scraper](https://www.ulta.com/)
- [Sephora Scraper](https://www.sephora.com/)


## Add a New Spider or Feature


If you want to add a spider/scraper to the app or even a new feature please use the link bellow or open it as an issue in this github repo. Most upvoted feature will be added to the app.

> [Add new spider or feature](https://vote.hnmedia.io/)


## Upcoming Scraper/Spiders


- [verishop Scraper](https://www.verishop.com/)
- [uncommongoods Scraper](https://www.uncommongoods.com/)


## Contribution


You are most welcome to contribute to this project and create pull requests.


## Credit


- [@diemonster](https://github.com/diemonster) for all his comments, feedbacks and instruction.
- Everyone in the `#python` community in the [libera IRC](https://libera.chat)

## Disclimar


This library is built for educational puposes ONLY, use at your own risk.
