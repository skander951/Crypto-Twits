import os
import time
import pandas as pd
from datetime import datetime
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup

OUTPUT_FILE = "/data/crypto_reddit.csv"
COINS = ["bitcoin", "ethereum", "cardano"]
INTERVAL = 300  # fetch every 5 minutes

def fetch_posts(coin):
    url = f"https://www.reddit.com/r/cryptocurrency/search/?q={coin}&restrict_sr=1&sort=new"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    posts = soup.find_all("h3")  # Reddit post titles
    rows = []
    for post in posts[:20]:  # top 20 recent posts
        text = post.get_text()
        sentiment = TextBlob(text).sentiment.polarity
        rows.append({
            "timestamp": datetime.utcnow(),
            "coin": coin,
            "post_text": text,
            "sentiment_score": sentiment
        })
    return rows

def main():
    os.makedirs("/data", exist_ok=True)
    while True:
        all_rows = []
        for coin in COINS:
            rows = fetch_posts(coin)
            all_rows.extend(rows)
        
        df = pd.DataFrame(all_rows)
        
        if os.path.exists(OUTPUT_FILE):
            df_existing = pd.read_csv(OUTPUT_FILE, parse_dates=["timestamp"])
            df = pd.concat([df_existing, df], ignore_index=True)
        
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"[{datetime.utcnow()}] Reddit sentiment saved.")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
