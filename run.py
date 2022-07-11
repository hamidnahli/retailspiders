from spiders.asos import Asos

if __name__ == '__main__':
    url = 'https://www.asos.com/adidas-originals/adidas-originals-streetball-ii-trainers-in-grey-tones-and-cream/prd/201271050?ctaref=we+recommend+grid_6&featureref1=we+recommend+pers'
    p = Asos(product_url=url)
    print(p.get_product_info())
    print(p.get_product_review())
