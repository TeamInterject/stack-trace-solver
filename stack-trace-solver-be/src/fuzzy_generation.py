import difflib
import re
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from exception_extractor import retrieve_exception_dictionary, load_exceptions
from exception_template import ExceptionTemplate
from knowledge_base import KnowledgeBase

def show_diff(seqm):
    output= []
    for opcode, a_start, a_end, _, _ in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a_start:a_end])
        elif opcode == 'insert':
            output.append("{*}")
        elif opcode == 'delete':
            output.append("{*}")
        elif opcode == 'replace':
            output.append("{*}")
        else:
            raise RuntimeError("unexpected opcode")
    return ''.join(output)


def fuzzy_group(exception_list, scorer, threshold):
    groups = []
    while len(exception_list) >= 2:
        matches = process.extract(exception_list[0], exception_list[1:], limit=1000, scorer=scorer)

        current_group = [match[0] for match in matches if match[1] >= threshold]
        current_group.append(exception_list[0])
        groups.append((current_group, threshold))

        exception_list = [match[0] for match in matches if match[1] < threshold]

    if len(exception_list) == 1:
        groups.append(([exception_list[0]], threshold))

    return groups

def generate_template(type, messages):
    if len(messages) == 1:
        return ExceptionTemplate(type, messages, messages[0])
    
    template = messages[0]
    for toCompareId in range(len(messages)):
        for other in messages[toCompareId+1:]:
            sm = difflib.SequenceMatcher(None, template, other)
            template = show_diff(sm)

    between_two_wildcards = r"(\{\*\}.{0,5}\{\*\})";
    next_to_wildcard = r"(((?<=\s)\S)?\{\*\}(\S(?=\s))?)"

    template = re.sub(next_to_wildcard, "{*}", template)
    while re.search(between_two_wildcards, template):
        template = re.sub(between_two_wildcards, "{*}", template)

    if "{*}" in template and len(template.replace("{*}", "")) <= 6:
        return None
    
    return ExceptionTemplate(type, messages, template, "{*}" in template)

def generate_templates(filename, scorer):
    ex_dict = retrieve_exception_dictionary(filename)
    ex_dict_keys = list(ex_dict.keys())
    ex_dict_keys.sort()
    exception_templates = []

    for key in ex_dict_keys:
        values = ex_dict[key]
        if len(values) < 1:
            continue

        all_messages = [value.message for value in values]
        print("Generating type:", key)
        message_groups = fuzzy_group(all_messages, scorer, 70)

        while len(message_groups) != 0:
            messages, used_threshold = message_groups.pop(0)
            template = generate_template(key, messages)
            if template is not None:
                exception_templates.append(template)
            else:
                regenerated_groups = fuzzy_group(messages, scorer, used_threshold + 3)
                while len(regenerated_groups) <= 1 and used_threshold <= 94:
                    _, used_threshold = regenerated_groups[0]
                    regenerated_groups = fuzzy_group(messages, scorer, used_threshold + 3)

                if len(regenerated_groups) > 1:
                    message_groups.extend(regenerated_groups)

    return exception_templates

def generate_with_debug(filename, scorer=fuzz.ratio):
    templates = generate_templates(filename, scorer)
    for template in templates:
        if not template.generated:
            continue
        
        print(template)
        for message in template.messages:
            print(f"\t{message}")

def generate_to_knowledge_base(filename, sqlite_filename="knowledge_base.sql", scorer=fuzz.ratio):
    templates = generate_templates(filename, scorer)

    base = KnowledgeBase(sqlite_filename)
    for template in templates:
        if not template.generated:
            continue
        
        base.insert_exception_template(template)

def load_to_knowledge_base(filename, sqlite_filename="knowledge_base.sql"):
    exceptions = load_exceptions(filename)
    templates = [ExceptionTemplate(exception.exception, [], exception.message) for exception in exceptions]

    base = KnowledgeBase(sqlite_filename)
    for template in templates:
        if "{*}" in template.template:
            base.insert_exception_template(template)

def generate_with_different_scorers():
    scorers = [fuzz.ratio, fuzz.token_set_ratio]

    for scorer in scorers:
        generate_to_knowledge_base("exceptions.txt", f"knowledge_base_{scorer.__name__}.sqlite", scorer)
        generate_to_knowledge_base("cas.txt", f"knowledge_base_{scorer.__name__}.sqlite", scorer)

def generate_single_with_different_scorers():
    scorers = [fuzz.ratio, fuzz.token_set_ratio]

    for scorer in scorers:
        pass
        generate_to_knowledge_base("exceptions.txt", "knowledge_base.sqlite", scorer)
        generate_to_knowledge_base("cas.txt", "knowledge_base.sqlite", scorer)

    load_to_knowledge_base("manual/sorted_finished_exceptions.txt", "knowledge_base.sqlite")

if __name__ == "__main__":
    # generate_with_different_scorers()
    generate_single_with_different_scorers()
    # load_to_knowledge_base("manual/sorted_finished_exceptions.txt")

