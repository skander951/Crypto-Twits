import requests
import pandas as pd
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

API_KEY = os.getenv("COINGECKO_API_KEY")
OUTPUT_FILE = "/data/crypto_data.csv"
COINS = ["bitcoin", "ethereum", "cardano"]
INTERVAL = 60  # seconds

def fetch_prices():
    url = "https://pro-api.coingecko.com/api/v3/simple/price"
    headers = {"X-Cg-Pro-Api-Key": API_KEY}  # use key from .env
    params = {
        "ids": ",".join(COINS),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def main():
    os.makedirs("/data", exist_ok=True)
    while True:
        data = fetch_prices()
        rows = []
        timestamp = datetime.utcnow()
        for coin, info in data.items():
            rows.append({
                "timestamp": timestamp,
                "coin": coin,
                "price": info["usd"],
                "change_24h": info["usd_24h_change"]
            })
        df = pd.DataFrame(rows)
        if os.path.exists(OUTPUT_FILE):
            df_existing = pd.read_csv(OUTPUT_FILE)
            df = pd.concat([df_existing, df], ignore_index=True)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"[{timestamp}] Data saved.")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
