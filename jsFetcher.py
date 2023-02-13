import requests
import os
import json
import argparse
import concurrent.futures
from fake_useragent import UserAgent
import time
import random


ua = UserAgent(browsers=['edge', 'chrome', 'safari', 'ie', 'firefox'])

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file containing list of endpoints")
parser.add_argument("path", help="path to dump the js files")
args = parser.parse_args()


def get_response(endpoint):
    headers = {
    "User-Agent": ua.random,
    "Accept": "text/html,application/xhtml+xml,application/xml",
    "Accept-Encoding":"gzip, deflate, br",
    "Referer": "https://www.google.com/"
    }
    delay = random.uniform(0, 2)
    time.sleep(delay)
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        filename = f"{endpoint.split('/')[-1]}"[:8] + '_' + f"{endpoint.split('/')[-1]}"[-8:] + ".js"
        filepath = os.path.join(folder_name, filename)
        with open(filepath, "w") as f:
            f.write(response.content)
    else:
        print(f"{endpoint} returned {response.status_code} status code")

with open(args.file) as file:
    endpoints = file.readlines()

folder_name = os.path.abspath(args.path)
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_response, endpoints)
