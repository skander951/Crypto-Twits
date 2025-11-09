import pandas as pd
import os

PRICE_FILE = "/data/crypto_data.csv"
REDDIT_FILE = "/data/crypto_reddit.csv"
OUTPUT_FILE = "/data/crypto_processed.csv"

def merge_data():
    # Load price data
    if not os.path.exists(PRICE_FILE):
        print("No price data found.")
        return
    df_price = pd.read_csv(PRICE_FILE, parse_dates=["timestamp"])
    
    # Load Reddit sentiment data
    if os.path.exists(REDDIT_FILE):
        df_reddit = pd.read_csv(REDDIT_FILE, parse_dates=["timestamp"])
        
        # Aggregate sentiment per coin per hour
        df_sentiment = (
            df_reddit
            .groupby(['coin', pd.Grouper(key='timestamp', freq='1H')])
            ['sentiment_score']
            .mean()
            .reset_index()
        )
        
        # Merge price and sentiment
        df_merged = pd.merge_asof(
            df_price.sort_values('timestamp'),
            df_sentiment.sort_values('timestamp'),
            by='coin',
            on='timestamp',
            direction='nearest'
        )
    else:
        df_merged = df_price
    
    # Add a simple moving average of the last 5 prices
    df_merged["sma_5"] = df_merged.groupby("coin")["price"].transform(lambda x: x.rolling(5).mean())
    
    # Save the merged data
    df_merged.to_csv(OUTPUT_FILE, index=False)
    print("Merged CoinGecko + Reddit sentiment data saved as crypto_processed.csv")

if __name__ == "__main__":
    merge_data()
