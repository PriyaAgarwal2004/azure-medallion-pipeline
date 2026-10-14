import json
import logging
import time
import requests

from config import BRONZE_DIR, CITIES, START_DATE, END_DATE, setup_logging


API_URL = "https://archive-api.open-meteo.com/v1/archive"
MAX_ATTEMPTS = 3

def extract_weather(latitude, longitude, start_date, end_date):
    """Download hourly weather history and return the raw JSON as a dictionary."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m",
    }
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(API_URL, params=params, timeout=(10, 60))
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logging.warning("Attempt %s of %s failed: %s", attempt, MAX_ATTEMPTS, e)
            if attempt == MAX_ATTEMPTS:
                logging.error("Extract failed after %s attempts", MAX_ATTEMPTS)
                raise
            time.sleep(2 ** attempt)          # wait 2 seconds, then 4
        except requests.exceptions.RequestException as e:
            logging.error("Extract failed: %s", e)    # other errors, like a 404, won't improve on retry
            raise


def save_bronze(raw, city):
    """Save the raw JSON, unchanged, into data/bronze/."""
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    file_path = BRONZE_DIR / f"weather_{city}.json"
    with open(file_path, "w") as f:
        json.dump(raw, f)
    return file_path


if __name__ == "__main__":
    setup_logging()
    logging.info("Extract started")
    for city, (lat, lon) in CITIES.items():
        raw = extract_weather(lat, lon, START_DATE, END_DATE)
        path = save_bronze(raw, city)
        logging.info("Saved %s rows to %s", len(raw["hourly"]["time"]), path)
        print("Saved", len(raw["hourly"]["time"]), "rows to", path)
    logging.info("Extract finished")