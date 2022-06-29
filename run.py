from spiders.asos import Asos

if __name__ == '__main__':
    
    # MISS RTYPE 
    url = 'https://www.asos.com/adidas-originals/adidas-originals-ozrah-trainers-in-pale-nude/prd/201136102?colourWayId=201136103&cid=1935'
    p = Asos(product_url=url)
    print(p.get_product_info())
    #https://www.asos.com/api/product/reviews/v1/products/202952871?offset=10&limit=20&include=Products&store=US&lang=en-US&filteredStats=reviews&sort=SubmissionTime:desc
