import requests
from app.logger import setup_logger

logger = setup_logger(__name__)


def get_weather(latitude: float, longitude: float) -> str:
    """
    Method to fetch weather from third party service
    """
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    }

    logger.info("Fetching weather data...")
    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        logger.info("Data not found")
        return "Temperature and windspeed unavailable"

    logger.info("Data found")
    response.raise_for_status()

    weather = response.json()["current_weather"]

    return (
        f"Temperature {weather['temperature']}°C, "
        f"Windspeed {weather['windspeed']} km/h"
    )
