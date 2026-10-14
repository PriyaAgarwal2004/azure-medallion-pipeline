import pandas as pd
import pytest

from transform import validate_hourly


def make_hourly(temps):
    times = pd.date_range("2025-01-01", periods=len(temps), freq="h")
    return pd.DataFrame({"time": times, "temperature_2m": temps, "city": "pune"})


def test_good_data_passes():
    validate_hourly(make_hourly([20.0, 21.5, 19.0]), "pune")   # should not raise


def test_missing_temperature_is_rejected():
    with pytest.raises(ValueError, match="missing temperatures"):
        validate_hourly(make_hourly([20.0, None, 19.0]), "pune")


def test_impossible_temperature_is_rejected():
    with pytest.raises(ValueError, match="outside"):
        validate_hourly(make_hourly([20.0, 900.0]), "pune")