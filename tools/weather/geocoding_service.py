import requests
from typing import Any

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def geocode_location(location: str) -> dict[str, Any]:
    params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(GEOCODING_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        raise ValueError(f"Location not found: {location}")

    result = data["results"][0]

    return {
        "name": result["name"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "country": result.get("country"),
        "timezone": result.get("timezone")
    }


# if __name__ == "__main__":
#     # Simple test for geocode_location
#     test_location = "New York"
#     try:
#         result = geocode_location(test_location)
#         print(f"Geocoding result for '{test_location}':")
#         for k, v in result.items():
#             print(f"  {k}: {v}")
#     except Exception as e:
#         print(f"Error: {e}")
