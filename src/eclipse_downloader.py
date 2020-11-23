from time import sleep
import requests
from datetime import datetime, timedelta
import time
import os.path
import random
import _thread
from tqdm import tqdm
from utils import chunks

def generate_file_name(id):
    return f"ignored_data/downloads/incident_{id:06d}.xml"

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
     
        expected_time = datetime.now() + timedelta(seconds=0.1)
        response = requests.get(f"https://bugs.eclipse.org/bugs/show_bug.cgi?ctype=xml&id={id}")

        if not response.ok:
            need_retry = True
            continue

        with open(file_name, "w+", encoding="utf-8") as file:
            try:
                file.write(response.content.decode("utf-8"))
            except:
                file.close()
                os.remove(file.name)
                raise

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
            print(Ex)
            continue
        finally:
            time.sleep(5)

def orchestrate_download():
    if not os.path.exists('ignored_data/downloads'):
        os.makedirs('ignored_data/downloads')

    splits = 4
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

orchestrate_download()