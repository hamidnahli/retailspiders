from typing import Any, Dict

import pandas as pd
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode


def convert_file_to_list(filelocation):
    urls = None
    if filelocation.endswith('.csv'):
        df = pd.read_csv(filelocation)
        urls = df['products'].to_list()
    elif filelocation.endswith('.xlsx'):
        df = pd.read_excel(filelocation)
        urls = df['products'].to_list()
    else:
        print('Currently only csv and excel file format are supported')
    return urls


def save_as(data, data_type, extension):
    df = None
    if isinstance(data, dict):
        df = pd.DataFrame(data, index=[0])
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    if extension == 'csv':
        df.to_csv(f'{data_type}.csv')
    elif extension == 'xlsx':
        df.to_excel(f'{data_type}.xlsx')
    elif extension == 'json':
        df.to_json(f'{data_type}.json', orient="records", indent=4)


def get_next_url(url: str, param: str, nxt: int):
    url_parse = urlparse(url)
    query = url_parse.query
    url_dict: Dict[str, Any] = dict(parse_qsl(query))
    if isinstance(url_dict[param], list):
        page = int(url_dict[param][0]) + nxt
    else:
        page = int(url_dict[param]) + nxt
    params = {param: page}
    url_dict.update(params)
    url_new_query = urlencode(url_dict)
    url_parse = url_parse._replace(query=url_new_query)
    next_url = urlunparse(url_parse)
    return next_url


