from spiders.rei import Rei
from test import ReiModel
from items.utils import parse_robots_txt
from items.proxy import start_session


if __name__ == '__main__':
    #url = 'https://www.rei.com/product/146801/patagonia-capilene-cool-daily-hoodie-mens'
    #p = Rei(product_url=url)
    #p.get_product_info(proxy=True)
    
    # data_review = p.get_product_review()
    #p = ReiModel()
    # p.create_tables()
    # p.insert(data_review,data_product)
    
    url = 'https://www.rei.com/'
    # urls = parse_robots_txt(url, identifier = 'product/')
    # print(urls)
    # print(len(urls))
    gateway, session = start_session(url)
    p = Rei(url, session = session)
    p.get_product_info()


    