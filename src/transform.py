import json
from pathlib import Path
import logging
import pandas as pd

from config import BRONZE_DIR, SILVER_DIR, CITIES, setup_logging

def transform_weather(city):
    """Read a bronze JSON file and return a clean table (DataFrame)."""
    with open(BRONZE_DIR / f"weather_{city}.json") as f:
        raw = json.load(f)

    df = pd.DataFrame(raw["hourly"])           # two lists become two columns
    df["time"] = pd.to_datetime(df["time"])    # text becomes real date-times
    df["city"] = city                          # label every row with its city
    validate_hourly(df, city)
    return df


def save_silver(df, city):
    """Save the clean table as a Parquet file in data/silver/."""
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    file_path = SILVER_DIR / f"weather_{city}.parquet"
    df.to_parquet(file_path, index=False)
    return file_path

def validate_hourly(df, city):
    """Stop the pipeline if the data looks wrong."""
    problems = []

    if df["temperature_2m"].isna().any():
        problems.append("missing temperatures")
    if df["time"].duplicated().any():
        problems.append("duplicate timestamps")
    if not df["temperature_2m"].dropna().between(-50, 60).all():
        problems.append("temperature outside -50 to 60 C")

    if problems:
        raise ValueError(f"{city}: " + ", ".join(problems))


if __name__ == "__main__":
    setup_logging()
    logging.info("Transform started")
    for city in CITIES:
        try:
            df = transform_weather(city)
        except ValueError as e:
            logging.error("Validation failed: %s", e)    # record why, then stop
            raise
        path = save_silver(df, city)
        logging.info("Saved %s rows to %s", len(df), path)
        print("Saved", len(df), "rows to", path)
    logging.info("Transform finished")