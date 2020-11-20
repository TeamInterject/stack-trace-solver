import requests
from datetime import datetime, timedelta
import time
import os.path
import random


def generate_file_name(id):
    return f"./downloads/incident_{id:06d}.xml"


def get_missing_file_ids():
    array_of_missing = []
    for id in range(1, 569009):
        file_name = generate_file_name(id)
        if not os.path.isfile(file_name):
            array_of_missing.append(id)

    random.shuffle(array_of_missing)
    return array_of_missing


def download_stacks():
    ids = get_missing_file_ids()
    need_retry = False

    for id in ids:
        file_name = generate_file_name(id)

        expected_time = datetime.now() + timedelta(seconds=1)
        response = requests.get(f"https://bugs.eclipse.org/bugs/show_bug.cgi?ctype=xml&id={id}")

        if not response.ok:
            need_retry = True
            continue

        with open(file_name, "w+") as file:
            file.write(response.content.decode("utf-8"))

        current_time = datetime.now()
        if expected_time > current_time:
            inter = expected_time - current_time
            time.sleep(inter.microseconds / 1000000)

    return need_retry


need_download = True
while need_download:
    try:
        need_download = download_stacks()
    except Exception as Ex:
        print(Ex)
        continue
    finally:
        time.sleep(120)
