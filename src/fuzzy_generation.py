import difflib
import re
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from exception_extractor import retrieve_exception_dictionary, load_exceptions
from exception_template import ExceptionTemplate
from knowladge_base import KnowladgeBase

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


def fuzzy_group(exception_list):
    groups = []
    while len(exception_list) >= 2:
        matches = process.extract(exception_list[0], exception_list[1:], limit=1000, scorer=fuzz.ratio)

        current_group = [match[0] for match in matches if match[1] >= 70]
        current_group.append(exception_list[0])
        groups.append(current_group)

        exception_list = [match[0] for match in matches if match[1] < 70]

    if len(exception_list) == 1:
        groups.append([exception_list[0]])

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
    
    return ExceptionTemplate(type, messages, template, True)

def generate_templates(filename):
    ex_dict = retrieve_exception_dictionary(filename)
    ex_dict_keys = list(ex_dict.keys())
    ex_dict_keys.sort()
    exception_templates = []

    for key in ex_dict_keys:
        values = ex_dict[key]
        if len(values) < 1:
            continue

        all_messages = [value.message for value in values]
        message_groups = fuzzy_group(all_messages)
        for messages in message_groups:
            template = generate_template(key, messages)
            exception_templates.append(template)

    return exception_templates

def generate_with_debug(filename):
    templates = generate_templates(filename)
    for template in templates:
        if not template.generated:
            continue
        
        print(template)
        for message in template.messages:
            print(f"\t{message}")

def generate_to_knowladge_base(filename):
    templates = generate_templates(filename)

    base = KnowladgeBase()
    for template in templates:
        if not template.generated:
            continue

        base.insert_exception_template(template)

def load_to_knowladge_base(filename):
    exceptions = load_exceptions(filename)
    templates = [ExceptionTemplate(exception.exception, [], exception.message) for exception in exceptions]

    base = KnowladgeBase()
    for template in templates:
        base.insert_exception_template(template)

#generate_with_debug("cas.txt")
#generate_to_knowladge_base("cas.txt")
#generate_to_knowladge_base("exceptions.txt")
#load_to_knowladge_base("sorted_finished_exceptions.txt")

