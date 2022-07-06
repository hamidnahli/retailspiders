from spiders.rei import Rei
from items.utils import parse_robots_txt

if __name__ == '__main__':
    url = 'https://www.rei.com/product/162208/co-op-cycles-drt-11-bike'
    p = Rei(product_url=url)
    #p.get_product_info(proxy=True)
    p.get_product_info()
    print(p.get_product_review())
    # url = 'https://ninewest.com/'
    # urls = parse_robots_txt(url)
    # print(urls)