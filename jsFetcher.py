import requests
import os
import json
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file containing list of endpoints")
args = parser.parse_args()

with open(args.file) as file:
    endpoints = file.readlines()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml",
    "Accept-Encoding":"gzip, deflate, br",
    "Referer": "https://www.google.com/"
}

folder_name = "js_endpoint_responses"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

for endpoint in tqdm(endpoints):
    endpoint = endpoint.strip()
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            filename = f"{endpoint.split('/')[-1]}.json"
            filepath = os.path.join(folder_name, filename)
            with open(filepath, "w") as f:
                json.dump(data, f)
        except json.decoder.JSONDecodeError as e:
            print(f"{endpoint} is not returning json data")
    else:
        print(f"{endpoint} returned {response.status_code} status code")

