from spiders.rei import Rei
from test import SpiderModel

if __name__ == '__main__':
    url = 'https://www.rei.com/product/146801/patagonia-capilene-cool-daily-hoodie-mens'
    p = Rei(product_url=url)
    data_product =  p.get_product_info()
    data_review = p.get_product_review()
    p = SpiderModel()
    #p.create_tables()
    p.insert(data_review,data_product)