from spiders.anthropologie import Anthropologie
from spiders.ninewest import NineWest

if __name__ == '__main__':
    #url = 'https://ninewest.com/products/speakup-almond-toe-flats-in-black-floral'
    #p = NineWest(product_url=url)
    #print(p.get_product_info())
    url = 'https://www.anthropologie.com/shop/facial-rounds?color=000&recommendation=home-hpg-tray-1-sfrectray-homepagetrendingmostpurchased&type=STANDARD&size=One%20Size&quantity=1'
    p = Anthropologie(product_url=url)
    print(p.get_product_info())
