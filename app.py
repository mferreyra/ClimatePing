from flask import Flask, render_template, redirect, url_for
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

app = Flask(__name__)


cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


@app.route("/")
def index():
    return redirect(url_for("get_weather"))


@app.route("/ping")
def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -34.9215,
        "longitude": -57.9545,
        "current": ["temperature_2m", "apparent_temperature", "precipitation"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"],
        "timezone": "America/Sao_Paulo",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_apparent_temperature = current.Variables(1).Value()
    current_precipitation = current.Variables(2).Value()

    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(2).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["precipitation_probability_max"] = daily_precipitation_probability_max

    daily_dataframe = pd.DataFrame(data=daily_data)

    return render_template("weather.html",
                           current_temperature_2m=current_temperature_2m,
                           current_apparent_temperature=current_apparent_temperature,
                           current_precipitation=current_precipitation,
                           daily_dataframe=daily_dataframe)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
