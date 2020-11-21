from regex_matchers import retrieve_exceptions
from utils import chunks
import threading
import glob
from pathlib import Path
import os

def extract_exceptions(files):
    for path in files:
        fileName = Path(path).stem
        outputFile = "exceptions/{fileName}.txt"
        if os.path.isfile(outputFile):
            continue

        with open(path, "r+", encoding="utf-8", errors='ignore') as file:
            lines = "\n".join(file.readlines())
            excs = retrieve_exceptions(lines)
            if len(excs) == 0:
                continue
            
            print(path)
            with open(f"exceptions/{fileName}.txt", "a", encoding="utf-8", errors="ignore") as output:
                for exception in excs:
                    output.write(exception.__str__() + "\n")

def orchestrate_extraction(threads=8):
    files = glob.glob("./downloads/*.xml")
    files.sort()
    chunked_files = chunks(files, threads)

    threads = []
    for chunk in chunked_files:
        t = threading.Thread(target=extract_exceptions, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    files = glob.glob("exceptions/*.txt")
    for path in files:
        with open(f"exceptions.txt", "a", encoding="utf-8", errors="ignore") as output:
            with open(path, "r+", encoding="utf-8", errors='ignore') as file:
                lines = "\n".join(file.readlines())
                output.write(lines)

def load_exceptions():
    with open("exeptions.txt", "r+", encoding="utf-8", errors='ignore') as file:
        lines = "\n".join(file.readlines())
        return retrieve_exceptions(lines)

orchestrate_extraction()