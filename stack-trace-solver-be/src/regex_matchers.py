import re

def check_for_java(text):
    return bool(re.search(r"((.|\n)*)[(].*\.java.*[)]((.|\n)*)", text))

class ExceptionMatch(object):
    def __init__(self, exception, msg=""):
        self.exception = exception.strip()
        self.message = msg.strip()

    def __str__(self):
        if self.message == "":
            return self.exception

        return f"{self.exception}: {self.message}"

    def __repr__(self):
        return self.__str__()

def retrieve_exceptions(text):
    searches = re.findall(
        r"((?:\b\w*\.*)*?\w*(?:Exception|Error))(?:(?:\n)|(?:(?::)(.*\n)))", text, re.MULTILINE)
    return [ExceptionMatch(match[0], match[1]) for match in searches]
