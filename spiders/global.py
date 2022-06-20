import requests
import json
global_headers = {
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,de;q=0.6',
}
response=requests.get('https://www.bestbuy.com/site/apple-iphone-13-5g-128gb-pink-sprint/6443067.p?skuId=6443067#anchor=productVariations',headers=global_headers)
