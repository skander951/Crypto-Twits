import pandas as pd
import os

MERGED_FILE = "/data/merged.csv"
PRED_FILE = "/data/predictions.csv"

if not os.path.exists(MERGED_FILE):
    print("No merged data found. Run preprocessor first.")
    exit(0)

df = pd.read_csv(MERGED_FILE)
df['prediction'] = 0.5  # dummy prediction
df.to_csv(PRED_FILE, index=False)
print(f"✅ Predictions saved to {PRED_FILE}")
