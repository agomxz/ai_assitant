from unittest.mock import patch, Mock

from app.tools.get_weather import get_weather

@patch("app.tools.get_weather.requests.get")
def test_get_weather_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "current_weather": {
            "temperature": 25.5,
            "windspeed": 10.2,
        }
    }
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = get_weather(19.4326, -99.1332)

    assert result == "Temperature 25.5°C, Windspeed 10.2 km/h"

    mock_get.assert_called_once_with(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 19.4326,
            "longitude": -99.1332,
            "current_weather": True,
        },
        timeout=10,
    )
