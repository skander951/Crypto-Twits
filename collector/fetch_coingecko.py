import requests
import pandas as pd
from datetime import datetime, timezone
import time
import os

OUTPUT_FILE = "/data/crypto_data.csv"
COINS = ["solana", "ethereum", "cardano"]
INTERVAL = 60  # seconds

def fetch_prices():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ",".join(COINS),
        "order": "market_cap_desc",
        "per_page": len(COINS),
        "page": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        print(response.status_code, response.text)  # <- debug
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            print("No valid data returned from API.")
            return []

        return data

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return []

def save_to_csv(rows):
    """Append new rows to CSV, creating it with header if it doesn't exist."""
    df = pd.DataFrame(rows)
    if os.path.exists(OUTPUT_FILE):
        try:
            df_existing = pd.read_csv(OUTPUT_FILE)
            df = pd.concat([df_existing, df], ignore_index=True)
        except pd.errors.EmptyDataError:
            print("Existing CSV is empty, creating new one.")
    else:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

def main():
    while True:
        data = fetch_prices()
        if not data:
            print(f"[{datetime.now(datetime.timezone.utc)}] No data received, retrying in {INTERVAL}s...")
            time.sleep(INTERVAL)
            continue

        timestamp = datetime.now(timezone.utc)
        rows = []
        for crypto in data:
            rows.append({
                "timestamp": timestamp,
                "coin": crypto.get("id"),
                "price": crypto.get("current_price"),
                "change_24h": crypto.get("price_change_percentage_24h")
            })

        save_to_csv(rows)
        print(f"[{timestamp}] Data saved for {len(rows)} coins.")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()


