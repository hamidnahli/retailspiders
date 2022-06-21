from spiders.ninewest import NineWest

if __name__ == '__main__':
    url = 'https://ninewest.com/products/speakup-almond-toe-flats-in-black-floral'
    p = NineWest(product_url=url)
    print(p.get_product_info())
