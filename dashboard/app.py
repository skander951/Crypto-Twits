from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from flask import Flask

# Flask server
server = Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname='/')

DATA_FILE = "/data/crypto_processed.csv"

def load_data():
    try:
        df = pd.read_csv(DATA_FILE, parse_dates=["timestamp"])
        return df
    except:
        return pd.DataFrame()

# Dashboard layout
app.layout = html.Div([
    html.H1("Crypto Dashboard"),
    dcc.Interval(id="interval-component", interval=60*1000, n_intervals=0),  # refresh every 1 min
    dcc.Graph(id="price-trends"),
    dcc.Graph(id="top-movers"),
    dcc.Graph(id="reddit-sentiment-heatmap")
])

# Callbacks to update charts
@app.callback(
    [Output("price-trends", "figure"),
     Output("top-movers", "figure"),
     Output("reddit-sentiment-heatmap", "figure")],
    [Input("interval-component", "n_intervals")]
)
def update_dashboard(n):
    df = load_data()
    if df.empty:
        return {}, {}, {}

    # 1️⃣ Price trend line
    fig_price = px.line(df, x="timestamp", y="price", color="coin", title="Price Trends")

    # 2️⃣ Top gainers/losers (latest timestamp)
    latest = df[df.timestamp == df.timestamp.max()]
    fig_movers = px.bar(latest, x="coin", y="change_24h", color="change_24h",
                        title="Top Gainers / Losers", color_continuous_scale="RdYlGn")

    # 3️⃣ Reddit sentiment heatmap
    # Aggregate sentiment per coin for the last 24 hours
    last_24h = df[df.timestamp >= df.timestamp.max() - pd.Timedelta(hours=24)]
    heatmap_data = last_24h.groupby("coin")["sentiment_score"].mean().reset_index()
    fig_sentiment = px.imshow(
        [heatmap_data["sentiment_score"]],
        labels={"x": "Coin", "y": "Sentiment Score"},
        x=heatmap_data["coin"],
        y=["Sentiment"],
        color_continuous_scale="RdYlGn",
        text_auto=True,
        title="Reddit Sentiment Heatmap (Last 24h)"
    )

    return fig_price, fig_movers, fig_sentiment

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050)
