import sqlite3
from pathlib import Path

import pandas as pd

from config import SILVER_DIR, GOLD_DB, CITIES

TEMP_COLS = ["avg_temp", "min_temp", "max_temp"]


def load_silver(cities):
    """Read each city's silver file and stack them into one table."""
    frames = [pd.read_parquet(SILVER_DIR / f"weather_{city}.parquet") for city in cities]
    return pd.concat(frames, ignore_index=True)


def build_daily(df):
    """Turn hourly rows into one row per city per day."""
    df = df.copy()                                        # don't change the caller's table
    df["date"] = df["time"].dt.strftime("%Y-%m-%d")       # date as text, e.g. 2025-01-01

    daily = df.groupby(["city", "date"]).agg(
        avg_temp=("temperature_2m", "mean"),
        min_temp=("temperature_2m", "min"),
        max_temp=("temperature_2m", "max"),
    ).reset_index()

    daily[TEMP_COLS] = daily[TEMP_COLS].round(1)          # one decimal is enough

    if not (daily["min_temp"] <= daily["max_temp"]).all():
        print("Warning: some days have min_temp above max_temp")
    return daily


def save_gold(daily, db_path):
    """Upsert the daily table: update existing days, insert new ones."""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_weather (
            city     TEXT,
            date     TEXT,
            avg_temp REAL,
            min_temp REAL,
            max_temp REAL,
            PRIMARY KEY (city, date)
        )
    """)

    columns = ["city", "date", "avg_temp", "min_temp", "max_temp"]
    rows = list(daily[columns].itertuples(index=False, name=None))

    conn.executemany("""
        INSERT INTO daily_weather (city, date, avg_temp, min_temp, max_temp)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT (city, date) DO UPDATE SET
            avg_temp = excluded.avg_temp,
            min_temp = excluded.min_temp,
            max_temp = excluded.max_temp
    """, rows)

    conn.commit()
    conn.close()


def run_query(db_path, query):
    """Run a SQL query and return the result as a table."""
    conn = sqlite3.connect(db_path)
    result = pd.read_sql(query, conn)
    conn.close()
    return result


YEARLY_SUMMARY = """
SELECT city,
       ROUND(AVG(avg_temp), 1) AS year_avg,
       MIN(min_temp) AS coldest,
       MAX(max_temp) AS hottest
FROM daily_weather
GROUP BY city
"""


if __name__ == "__main__":
    hourly = load_silver(CITIES)
    daily = build_daily(hourly)
    save_gold(daily, GOLD_DB)
    print("Saved", len(daily), "rows to", GOLD_DB)
    print(run_query(GOLD_DB, "SELECT COUNT(*) AS rows_in_table FROM daily_weather"))
    print(run_query(GOLD_DB, YEARLY_SUMMARY))