import requests
import json
import re
from knowladge_base import KnowladgeBase

def get_stackoverflow_links(keyword, tags = []):
    BASEURL = "https://api.stackexchange.com/2.2/search/advanced"

    params = {
        "page": "1",
        "pagesize": "5",
        "order": "desc",
        "sort": "relevance",
        "q": keyword,
        "tagged": " ".join(tags),
        "site": "stackoverflow"
    }

    r = requests.get(BASEURL, params=params)

    temp = json.dumps(r.json(), indent=4, sort_keys=True)
    result = json.loads(temp)
    return result


# knowladge_base = {
#     "java.lang.NumberFormatException": [r'(For input string)(?:.+)'],
#     "java.sql.SQLException": [r'(Violation of unique constraint )(?:.+ )(duplicate value\(s\) for column\(s\) )(?:.+ )(in statement) (?:.+)'],
# }

knowladge_base = KnowladgeBase().get_knowladge_dict()

def format_stackoverflow_query_string(exception, message):
    if exception not in knowladge_base:
        # TODO: Do more processing. Tokenize, try to get rid of irregular words, etc.
        return message

    for fact in knowladge_base[exception]:
        found = re.search(fact, message)
        if bool(found):
            msg = "".join(found.groups())
            return [f"{exception}: {msg}", msg]
    
    return message