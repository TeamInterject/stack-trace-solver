from fuzzywuzzy.fuzz import token_set_ratio
from eclipse_downloader import orchestrate_download
from fuzzy_generation import generate_with_debug
from knowledge_base import KnowledgeBase

if __name__ == "__main__":
    ratio = KnowledgeBase("dynamic_threshold/knowledge_base_ratio.sqlite")
    token = KnowledgeBase("dynamic_threshold/knowledge_base_token_set_ratio.sqlite")

    ratio_dict = ratio.get_knowledge_dict()
    token_dict = token.get_knowledge_dict()

    key_set = set(ratio_dict.keys())
    key_set.update(token_dict.keys())
    key_set = list(key_set)
    key_set = sorted(key_set)

    for key in key_set:
        ratio_templates = ratio_dict.get(key, None)
        token_templates = token_dict.get(key, None)

        print("RATIO")
        if ratio_templates is not None:
            for template in ratio_templates:
                print(template)

        print("------------------------")
        print("TOKEN")
        if token_templates is not None:
            for template in token_templates:
                print(template)

        input()

    pass