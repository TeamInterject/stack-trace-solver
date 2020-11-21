from time import sleep
import requests
from datetime import datetime, timedelta
import time
import os.path
import random
import _thread
from tqdm import tqdm

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


def download_stacks(chunk):
    need_retry = False

    done = 0
    for id in chunk:
        file_name = generate_file_name(id)
        #print(f"{done}/{len(ids)}. Downloading report {id} to {file_name}...", end=" ")

        expected_time = datetime.now() + timedelta(seconds=0.1)
        response = requests.get(f"https://bugs.eclipse.org/bugs/show_bug.cgi?ctype=xml&id={id}")

        if not response.ok:
            need_retry = True
            #print("Failed.")
            continue

        with open(file_name, "w+", encoding="utf-8") as file:
            try:
                file.write(response.content.decode("utf-8"))
            except:
                #print("Failed.")
                file.close()
                os.remove(file.name)
                raise

        #print("Done.")

        current_time = datetime.now()
        if expected_time > current_time:
            inter = expected_time - current_time
            time.sleep(inter.microseconds / 1000000)

        done += 1

    return need_retry

def download_with_retry(chunk):
    need_download = True
    while need_download:
        try:
            need_download = download_stacks(chunk)
        except Exception as Ex:
            continue
        finally:
            time.sleep(5)

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

splits = 24
missing_files = get_missing_file_ids(0, 189669)
total_left = len(missing_files)
tbar = tqdm(total=total_left)
chunked = chunks(missing_files, splits)

for chunk in chunked:
    _thread.start_new_thread(download_with_retry, (chunk,))

while True:
    current_left = total_left - len(get_missing_file_ids(0, 189669))
    tbar.update(current_left - tbar.n)
    sleep(0.5)
    pass