import json
import re
# import requests
from ten_requests_skills import parse_url
from pprint import pprint

url = "https://pm.3.cn/prices/mgets?origin=3&ext=01000000&skuids=1399903,27269595515,42010078901,2372300,100006388460,41220088267,2502890,35509125811,11803445806,25786381619&source=fashionv4"
html_str = parse_url(url)
# print(html_str)
ret1 = json.loads(html_str)
pprint(ret1)
print(type(ret1))

