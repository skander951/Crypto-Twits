from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from flask import Flask

server = Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname='/')

DATA_FILE = "/data/crypto_processed.csv"

def load_data():
    try:
        df = pd.read_csv(DATA_FILE, parse_dates=["timestamp"])
        return df
    except:
        return pd.DataFrame()

app.layout = html.Div([
    html.H1("Crypto Dashboard"),
    dcc.Interval(id="interval-component", interval=60*1000, n_intervals=0),
    dcc.Graph(id="price-trends"),
    dcc.Graph(id="top-movers")
])

@app.callback(
    [Output("price-trends", "figure"),
     Output("top-movers", "figure")],
    [Input("interval-component", "n_intervals")]
)
def update_dashboard(n):
    df = load_data()
    if df.empty:
        return {}, {}
    
    fig_price = px.line(df, x="timestamp", y="price", color="coin", title="Price Trends")

    latest = df[df.timestamp == df.timestamp.max()]
    fig_movers = px.bar(latest, x="coin", y="change_24h", color="change_24h",
                        title="Top Gainers / Losers", color_continuous_scale="RdYlGn")

    return fig_price, fig_movers

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
