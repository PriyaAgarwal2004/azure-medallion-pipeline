import sqlite3
import pandas as pd
from gold import build_daily, save_gold


def make_hourly():
    """Two cities, two days each: 48 hourly rows per city."""
    times = pd.date_range("2025-01-01", periods=48, freq="h")
    frames = []
    for city in ["pune", "mumbai"]:
        frames.append(pd.DataFrame({
            "time": times,
            "temperature_2m": [20.0] * 48,
            "city": city,
        }))
    return pd.concat(frames, ignore_index=True)


def test_one_row_per_city_per_day():
    daily = build_daily(make_hourly())
    assert len(daily) == 4      # 2 cities x 2 days


def test_min_avg_max_values():
    times = pd.date_range("2025-01-01", periods=24, freq="h")
    temps = [10.0] * 12 + [30.0] * 12        # half the day at 10, half at 30
    hourly = pd.DataFrame({"time": times, "temperature_2m": temps, "city": "pune"})

    daily = build_daily(hourly)
    row = daily.iloc[0]                      # the only row: one city, one day

    assert row["date"] == "2025-01-01"
    assert row["min_temp"] == 10.0
    assert row["max_temp"] == 30.0
    assert row["avg_temp"] == 20.0           # (12 x 10 + 12 x 30) / 24


def test_upsert_updates_without_duplicating(tmp_path):
    db = str(tmp_path / "test.db")           # a throwaway database file

    day = pd.DataFrame({
        "city": ["pune"], "date": ["2025-01-01"],
        "avg_temp": [20.0], "min_temp": [10.0], "max_temp": [30.0],
    })
    save_gold(day, db)                        # first load

    corrected = day.copy()
    corrected["avg_temp"] = 25.0              # same day, new value
    save_gold(corrected, db)                  # second load

    conn = sqlite3.connect(db)
    count, avg = conn.execute(
        "SELECT COUNT(*), MAX(avg_temp) FROM daily_weather"
    ).fetchone()
    conn.close()

    assert count == 1                         # no duplicate row
    assert avg == 25.0                        # the value was updated