import requests
import json


def get_stackoverflow_links(keyword):
    BASEURL = "https://api.stackexchange.com/2.2/search"

    params = {
        "page": "1",
        "pagesize": "5",
        "order": "desc",
        "sort": "relevance",
        "intitle": keyword,
        "tagged": "java",
        "site": "stackoverflow"
    }

    r = requests.get(BASEURL, params=params)

    temp = json.dumps(r.json(), indent=4, sort_keys=True)
    result = json.loads(temp)
    return result