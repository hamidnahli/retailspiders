from spiders.ninewest import NineWest
from items.utils import parse_robots_txt

if __name__ == '__main__':
    url = 'https://ninewest.com/products/speakup-almond-toe-flats-in-black-floral'
    p = NineWest(product_url=url)
    p.get_product_info(proxy=True)
    # print(p.get_product_info())
    # url = 'https://ninewest.com/'
    # urls = parse_robots_txt(url)
    # print(urls)