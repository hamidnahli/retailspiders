from spiders.rei import Rei

if __name__ == '__main__':
    url = 'https://www.rei.com/product/146801/patagonia-capilene-cool-daily-hoodie-mens'
    p = Rei(product_url=url)
    print(p.get_product_info())
    print(p.get_product_review())
