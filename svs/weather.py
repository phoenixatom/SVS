# weather.py
from typing import Dict, Any

import openmeteo_requests
import requests_cache
from retry_requests import retry

weather_codes = {
    0: "☀️ Clear Sky",
    1: "🌤️ Partly Cloudy",
    2: "🌤️ Partly Cloudy",
    3: "🌥️ Overcast",
    45: "🌫️ Fog",
    48: "🌫️ Fog",
    51: "🌧️ Drizzle: Light",
    53: "🌧️ Drizzle: Moderate",
    55: "🌧️ Drizzle: Heavy",
    56: "❄️ Freezing Drizzle: Light",
    57: "❄️ Freezing Drizzle: Heavy",
    61: "🌧️ Rain: Slight",
    63: "🌧️ Rain: Moderate",
    65: "🌧️ Rain: Heavy",
    66: "❄️ Freezing Rain: Light",
    67: "❄️ Freezing Rain: Heavy",
    71: "🌨️ Snowfall: Slight",
    73: "🌨️ Snowfall: Moderate",
    75: "🌨️ Snowfall: Heavy",
    77: "❄️ Snow Grains",
    80: "🌧️ Rain Showers: Slight",
    81: "🌧️ Rain Showers: Moderate",
    82: "🌧️ Rain Showers: Violent",
    85: "🌨️ Snow Showers: Slight",
    86: "🌨️ Snow Showers: Heavy",
    95: "⛈️ Thunderstorm: Slight or Moderate",
    96: "⛈️ Thunderstorm with Slight Hail",
    99: "⛈️ Thunderstorm with Heavy Hail",
}

def get_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "rain",
                    "showers", "weather_code", "cloud_cover", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"]
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Extract current weather values
    current = response.Current()
    current_weather = {
        "temperature_2m": current.Variables(0).Value(),
        "relative_humidity_2m": current.Variables(1).Value(),
        "apparent_temperature": current.Variables(2).Value(),
        "precipitation": current.Variables(3).Value(),
        "rain": current.Variables(4).Value(),
        "showers": current.Variables(5).Value(),
        "weather_code": current.Variables(6).Value(),
        "cloud_cover": current.Variables(7).Value(),
        "wind_speed_10m": current.Variables(8).Value(),
        "wind_direction_10m": current.Variables(9).Value(),
        "wind_gusts_10m": current.Variables(10).Value(),
    }
    return current_weather
