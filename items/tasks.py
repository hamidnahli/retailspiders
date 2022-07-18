from celery import Celery
from usp.tree import sitemap_tree_for_homepage

#from dba.ninewestmodel import NineWestModel

app = Celery('tasks', broker='amqp://guest@localhost//')


@app.task
def parse_robots_txt(url, identifier=None):
    urls = []
    tree = sitemap_tree_for_homepage(url)
    for page in tree.all_pages():
        urls.append(page.url)
    if identifier:
        urls = [url for url in urls if identifier in url]
    return urls


# @app.task
# def ninewest_insert_info(data, table):
#     nw = NineWestModel()
#     nw.insert(data, table)


# @app.task
# def ninewest_insert_review(data, table):
#     nw = NineWestModel()
#     nw.review_bulk_insert(data, table)