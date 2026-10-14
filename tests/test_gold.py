import pandas as pd

from gold import build_daily


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