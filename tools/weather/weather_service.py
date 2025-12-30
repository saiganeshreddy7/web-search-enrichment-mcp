from typing import Any
import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry
# import json

from tools.weather.geocoding_service import geocode_location


# Setup Open-Meteo client
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_by_location(location: str) -> dict[str, Any]:
    geo = geocode_location(location)

    params = {
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        "hourly": "temperature_2m",
        "timezone": "UTC"
    }

    responses = openmeteo.weather_api(OPEN_METEO_URL, params=params)
    response = responses[0]

    hourly = response.Hourly()
    temperature = hourly.Variables(0).ValuesAsNumpy()

    times = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )

    return {
        "location": geo["name"],
        "country": geo["country"],
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        "timezone": geo["timezone"],
        "hourly_temperature": [
            {"time": str(t), "temperature": float(temp)}
            for t, temp in zip(times, temperature)
        ][:5],
        "source": "open-meteo"
    }


# if __name__ == "__main__":
#     # Simple test for get_weather_by_location
#     test_location = "New York"
#     result = get_weather_by_location(test_location)
#     print(json.dumps(result, indent=2))
#     # try:
#     #     result = get_weather_by_location(test_location)
#     #     print(f"Weather result for '{test_location}':")
#     #     print(f"Location: {result['location']}, Country: {result['country']}")
#     #     print(f"Latitude: {result['latitude']}, Longitude: {result['longitude']}")
#     #     print(f"Timezone: {result['timezone']}")
#     #     print(f"Source: {result['source']}")
#     #     print("Hourly Temperatures (first 5):")
#     #     for entry in result['hourly_temperature'][:5]:
#     #         print(f"  {entry['time']}: {entry['temperature']}°C")
#     # except Exception as e:
#     #     print(f"Error: {e}")
