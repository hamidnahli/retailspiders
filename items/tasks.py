from celery import Celery
from usp.tree import sitemap_tree_for_homepage

app = Celery('tasks', broker='sqs://', broker_transport_options={'region': 'us-east-2'})


@app.task
def parse_robots_txt(url, identifier=None):
    urls = []
    tree = sitemap_tree_for_homepage(url)
    for page in tree.all_pages():
        urls.append(page.url)
    if identifier:
        urls = [url for url in urls if identifier in url]
    return urls
