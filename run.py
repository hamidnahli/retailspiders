from spiders.anthropologie import Anthropologie
from items.utils import parse_robots_txt

if __name__ == '__main__':
    url = 'https://www.anthropologie.com/shop/pilcro-the-icon-flare-low-rise-jeans?category=new-clothes&color=010&type=STANDARD&quantity=1'
    p = Anthropologie(product_url=url)
    print(p.get_product_info(proxy=True))
    print(p.get_product_review(proxy=True))

    # print(p.get_product_info())
    # url = 'https://ninewest.com/'
    # urls = parse_robots_txt(url)
    # print(urls)

