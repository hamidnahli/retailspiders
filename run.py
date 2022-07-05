from spiders.urbanoutfitters import Urbanoutfitters
from items.utils import parse_robots_txt

if __name__ == '__main__':
    url = 'https://www.urbanoutfitters.com/shop/standard-cloth-reverse-terry-quarter-zip-sweatshirt?category=mens-clothing&color=030&type=REGULAR&quantity=1'
    p = Urbanoutfitters(product_url=url)
    p.get_product_info(proxy=True)
    print(p.get_product_info())
    
    # url = 'https://ninewest.com/'
    # urls = parse_robots_txt(url)
    # print(urls)