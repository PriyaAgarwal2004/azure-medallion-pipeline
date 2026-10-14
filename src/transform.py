import json
from pathlib import Path

import pandas as pd

from config import BRONZE_DIR, SILVER_DIR, CITIES

def transform_weather(city):
    """Read a bronze JSON file and return a clean table (DataFrame)."""
    with open(BRONZE_DIR / f"weather_{city}.json") as f:
        raw = json.load(f)

    df = pd.DataFrame(raw["hourly"])           # two lists become two columns
    df["time"] = pd.to_datetime(df["time"])    # text becomes real date-times
    df["city"] = city                          # label every row with its city
    return df


def save_silver(df, city):
    """Save the clean table as a Parquet file in data/silver/."""
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    file_path = SILVER_DIR / f"weather_{city}.parquet"
    df.to_parquet(file_path, index=False)
    return file_path


if __name__ == "__main__":
    for city in CITIES:
        df = transform_weather(city)
        path = save_silver(df, city)
        print("Saved", len(df), "rows to", path)