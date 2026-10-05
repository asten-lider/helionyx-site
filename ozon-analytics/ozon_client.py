import os
import time
import requests

BASE_URL = "https://api-seller.ozon.ru"

def headers():
    return {
        "Client-Id": os.environ["OZON_CLIENT_ID"],
        "Api-Key": os.environ["OZON_API_KEY"],
        "Content-Type": "application/json",
    }

def post(path, payload, timeout=60, retries=4):
    last = None
    for attempt in range(retries):
        try:
            r = requests.post(BASE_URL + path, headers=headers(), json=payload, timeout=timeout)
            if r.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Ozon API error {path}: {last}")
