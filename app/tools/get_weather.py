import requests


def get_weather(latitude: float, longitude: float) -> str:
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    weather = response.json()["current_weather"]

    return (
        f"Temperatura {weather['temperature']}°C, "
        f"Viento {weather['windspeed']} km/h"
    )
