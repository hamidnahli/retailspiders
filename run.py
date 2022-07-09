from spiders.Glossier import Glossier

if __name__ == '__main__':
    
    url = 'https://www.glossier.com/products/lidstar'
    p =Glossier(product_url=url)
    print(p.get_product_info())
    print(p.get_product_review())
    
    
    
    
