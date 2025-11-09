import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib


DATA = '/data/merged.csv'
MODEL_OUT = '/data/model.joblib'


if __name__ == '__main__':
    if not os.path.exists(DATA):
        print('No data to train on')
        exit(1)
    df = pd.read_csv(DATA)
    # Create a toy binary label: price up in 24h? (requires historical data in real project)
    # Here we create a dummy target for the scaffold to run
    df = df.dropna(subset=['current_price'])
    df['target'] = (df['price_change_percentage_24h'] > 0).astype(int)
    X = df[['current_price', 'market_cap', 'total_volume', 'avg_sentiment']].fillna(0)
    y = df['target']
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(Xs, y)
    joblib.dump({'model': clf, 'scaler': scaler}, MODEL_OUT)
    print('Trained and saved model to', MODEL_OUT)