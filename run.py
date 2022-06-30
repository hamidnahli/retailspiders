from spiders.asos import Asos

if __name__ == '__main__':
    url = 'https://www.asos.com/adidas-originals/adidas-originals-ozelia-trainers-in-black-and-white/prd/200964288'
    p = Asos(product_url=url)
    print(p.get_product_info())
    print(p.get_product_review())

