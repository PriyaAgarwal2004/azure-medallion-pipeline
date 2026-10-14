import logging
from pathlib import Path

DATA_DIR = Path("data")
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DB = str(DATA_DIR / "gold.db")

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

# city name -> (latitude, longitude)
CITIES = {
    "pune": (18.52, 73.86),
    "mumbai": (19.07, 72.88),
}

def setup_logging():
    """Write log lines to pipeline.log, with a timestamp on each."""
    logging.basicConfig(
        filename="pipeline.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )