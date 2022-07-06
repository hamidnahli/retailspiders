from spiders.ninewest import NineWest
# from items.utils import parse_robots_txt
from items.tasks import parse_robots_txt

if __name__ == '__main__':
    url = 'https://ninewest.com/products/braydin-stretch-flat-sandals-in-natural?pr_prod_strat=description&pr_rec_id=30c3aa4f1&pr_rec_pid=5388332138540&pr_ref_pid=6654765203500&pr_seq=uniform'
    p = NineWest(product_url=url)
    p.get_product_review(proxy=True)
    # reviews = p.get_product_review(proxy=True)
    # print(reviews)
    # urls = parse_robots_txt.delay('https://ninewest.com')
