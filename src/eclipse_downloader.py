from time import sleep
import requests
from datetime import datetime, timedelta
import time
import os.path
import random
import _thread
import argparse

def generate_file_name(id):
    return f"./downloads/incident_{id:06d}.xml"


def get_missing_file_ids(from_id, to_id):
    array_of_missing = []
    for id in range(from_id, to_id):
        file_name = generate_file_name(id)
        if not os.path.isfile(file_name):
            array_of_missing.append(id)

    random.shuffle(array_of_missing)
    return array_of_missing


def download_stacks(from_id, to_id):
    ids = get_missing_file_ids(from_id, to_id)
    need_retry = False

    done = 0
    for id in ids:
        file_name = generate_file_name(id)
        print(f"{done}/{len(ids)}. Downloading report {id} to {file_name}...", end=" ")

        expected_time = datetime.now() + timedelta(seconds=0.1)
        response = requests.get(f"https://bugs.eclipse.org/bugs/show_bug.cgi?ctype=xml&id={id}")

        if not response.ok:
            need_retry = True
            print("Failed.")
            continue

        with open(file_name, "w+", encoding="utf-8") as file:
            try:
                file.write(response.content.decode("utf-8"))
            except:
                print("Failed.")
                file.close()
                os.remove(file.name)
                raise

        print("Done.")

        current_time = datetime.now()
        if expected_time > current_time:
            inter = expected_time - current_time
            time.sleep(inter.microseconds / 1000000)

        done += 1

    return need_retry

def download_with_retry(from_id, to_id):
    need_download = True
    while need_download:
        try:
            need_download = download_stacks(from_id, to_id)
        except Exception as Ex:
            print(Ex)
            continue
        finally:
            print("Sleeping 5s...")
            time.sleep(5)

splits = 12
total_start = 0
total_end = 189669

for i in range(splits):
    total = total_end - total_start
    split_amount = total / splits
    start = int(split_amount * i) + total_start
    end = int(split_amount * (i+1)) + total_start

    _thread.start_new_thread(download_with_retry, (start, end))

while True:
    sleep(1)
    pass