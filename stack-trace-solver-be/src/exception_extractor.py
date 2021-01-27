from regex_matchers import retrieve_exceptions
from utils import chunks
import threading
import glob
from pathlib import Path
import os

def extract_exceptions(files):
    for path in files:
        fileName = Path(path).stem
        outputFile = f"ignored_data/exceptions/{fileName}.txt"
        if os.path.isfile(outputFile):
            continue

        with open(path, "r+", encoding="utf-8", errors='ignore') as file:
            lines = "\n".join(file.readlines())
            excs = retrieve_exceptions(lines)
            if len(excs) == 0:
                continue

            print(path)
            with open(f"ignored_data/exceptions/{fileName}.txt", "a", encoding="utf-8", errors="ignore") as output:
                for exception in excs:
                    output.write(exception.__str__() + "\n")

def orchestrate_extraction(threads=8):
    files = glob.glob("ignored_data/downloads/*.xml")
    files.sort()
    chunked_files = chunks(files, threads)

    threads = []
    for chunk in chunked_files:
        t = threading.Thread(target=extract_exceptions, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    files = glob.glob("ignored_data/exceptions/*.txt")
    for path in files:
        with open(f"ignored_data/exceptions.txt", "a", encoding="utf-8", errors="ignore") as output:
            with open(path, "r+", encoding="utf-8", errors='ignore') as file:
                lines = "\n".join(file.readlines())
                output.write(lines)

def load_exceptions(filename):
    with open(f"ignored_data/{filename}", "r+", encoding="utf-8", errors='ignore') as file:
        lines = "\n".join(file.readlines())
        return retrieve_exceptions(lines)

def retrieve_exception_dictionary(filename):
    exceptions = load_exceptions(filename)
    ex_dict = {}
    for exception in exceptions:
        if exception.exception not in ex_dict:
            ex_dict[exception.exception] = []
        
        ex_dict[exception.exception].append(exception)

    return ex_dict

def debug_print(filename):
    ex_dict = retrieve_exception_dictionary(filename)
    ex_dict_keys = list(ex_dict.keys())
    ex_dict_keys.sort()
    for key in ex_dict_keys:
        values = ex_dict[key]
        if len(values) < 2:
            continue

        print(key)
        for value in values:
            print(f"\t{value}")

# debug_print("exceptions_minimized.txt")