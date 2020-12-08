import requests
import json
import re
from knowledge_base import KnowledgeBase

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


def generate_knowledge_base_entry(template):
    parts = template.split("{*}")

    processed_parts = []
    for part in parts:
        if (len(part) == 0):
            processed_parts.append(part)
            continue

        part = re.escape(part)
        part = f"({part})"

        processed_parts.append(part)

    return "(?:.+)".join(processed_parts)

class GeneratedQueries():
    def __init__(self, template, queries):
        self.template = template
        self.queries = queries

knowledge_base = KnowledgeBase("knowledge_base.sql").get_knowledge_dict()

def format_stackoverflow_query_string(exception, message):
    if message is None or str.isspace(message) or len(message) == 0:
        return [GeneratedQueries("", [exception])]

    if exception not in knowledge_base:
        # TODO: Do more processing. Tokenize, try to get rid of irregular words, etc.
        return [GeneratedQueries("", [f"{exception}: {message}", message])]

    knowledge_base[exception].sort(key=len, reverse=True)

    results = []
    results.append(GeneratedQueries("", [f"{exception}: {message}"]))

    for fact in knowledge_base[exception]:
        fact_regex = generate_knowledge_base_entry(fact)

        found = re.search(fact_regex, message)
        if bool(found):
            msg = "".join(found.groups())
            if str.isspace(msg):
                pass

            results.append(GeneratedQueries(fact, [f"{exception}: {msg}", msg]))

    results.append(GeneratedQueries("", [message]))
    
    return results