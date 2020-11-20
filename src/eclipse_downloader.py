import requests
from datetime import datetime, timedelta
import time
import os.path

def download_stacks():
  for id in range(1, 100):
    file_name = f"./downloads/incident_{id:06d}.xml"
    if os.path.isfile(file_name):
      continue

    expected_time = datetime.now() + timedelta(seconds=1)
    response = requests.get(f"https://bugs.eclipse.org/bugs/show_bug.cgi?ctype=xml&id={id}")

    with open(file_name, "w+") as file:
      file.write(response.content.decode("utf-8"))

    current_time = datetime.now()
    if expected_time > current_time:
      inter = expected_time - current_time
      time.sleep(inter.microseconds / 1000000)

finished = False
while finished:
  try:
    download_stacks()
    finished = True
  except:
    time.sleep(120)
    continue