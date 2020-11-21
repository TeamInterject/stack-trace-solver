import re
import glob


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


def extract_exceptions():
    files = glob.glob("./downloads/*.xml")
    for path in files:
        with open("exceptions.txt", "a", encoding="utf-8", errors="ignore") as output:
            with open(path, "r+", encoding="utf-8", errors='ignore') as file:
                lines = "\n".join(file.readlines())
                excs = retrieve_exceptions(lines)
                if len(excs) != 0:
                    print(path)
                for exception in excs:
                    output.write(exception.__str__() + "\n")


def load_exceptions():
    with open("exeptions.txt", "r+", encoding="utf-8", errors='ignore') as file:
        lines = "\n".join(file.readlines())
        return retrieve_exceptions(lines)
