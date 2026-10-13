import json
from pathlib import Path

import requests

API_URL = "https://archive-api.open-meteo.com/v1/archive"
BRONZE_DIR = Path("data/bronze")


def extract_weather(latitude, longitude, start_date, end_date):
    """Download hourly weather history and return the raw JSON as a dictionary."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m",
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()   # stop with a clear error if the status is not 200
    return response.json()


def save_bronze(raw, city):
    """Save the raw JSON, unchanged, into data/bronze/."""
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    file_path = BRONZE_DIR / f"weather_{city}.json"
    with open(file_path, "w") as f:
        json.dump(raw, f)
    return file_path


if __name__ == "__main__":
    raw = extract_weather(19.07, 72.88, "2025-01-01", "2025-12-31")
    path = save_bronze(raw, "mumbai")
    print("Saved", len(raw["hourly"]["time"]), "rows to", path)