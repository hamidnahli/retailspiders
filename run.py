from spiders.clinique import Clinique



if __name__ == '__main__':
    
    url = 'https://www.clinique.com/product/4034/87057/skincare/serum/clinique-smart-clinical-repairtm-wrinkle-correcting-serum?size=1.7_oz._%2F_50_ml'
    p =Clinique(product_url=url)
    print(p.get_product_info())
    print(p.get_product_review())