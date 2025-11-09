🪙 Crypto Dashboard & Sentiment Monitor
📊 Overview

Crypto Dashboard & Sentiment Monitor is a real-time analytics platform that tracks cryptocurrency market movements and social sentiment.
It combines live price data from CoinGecko and Reddit sentiment analysis, then visualizes everything in an interactive Dash dashboard.

The system runs entirely in Docker Compose, with independent microservices handling data collection, preprocessing, and visualization.

⚙️ Features

    📈 Live Crypto Price Trends (via CoinGecko API)

    🚀 Top Gainers / Losers visualization

    💬 Reddit Sentiment Heatmap (without API key)

    ♻️ Automatic updates every minute

    🐳 Fully containerized — easy to run with docker-compose

🧩 Architecture
+---------------------------+
|   fetch_coingecko.py      | → Fetch crypto prices (CoinGecko API)
+---------------------------+
             │
             ▼
+---------------------------+
|    fetch_reddit.py        | → Scrape Reddit posts & analyze sentiment
+---------------------------+
             │
             ▼
+---------------------------+
|    merge_data.py          | → Merge prices + sentiment into CSV
+---------------------------+
             │
             ▼
+---------------------------+
|        app.py             | → Dash dashboard (visualization)
+---------------------------+
