import dotenv
import os
import requests
from datetime import datetime
from typing import List, Self, Dict, cast
from enum import Enum

dotenv.load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

class Weather_Icon(str, Enum):
    CLEAR_SKY_DAY = "01d"
    CLEAR_SKY_NIGHT = "01n"
    FEW_CLOUDS_DAY = "02d"
    FEW_CLOUDS_NIGHT = "02n"
    SCATTERED_CLOUDS_DAY = "03d"
    SCATTERED_CLOUDS_NIGHT = "03n"
    BROKEN_CLOUDS_DAY = "04d"
    BROKEN_CLOUDS_NIGHT = "04n"
    SHOWER_RAIN_DAY = "09d"
    SHOWER_RAIN_NIGHT = "09n"
    RAIN_DAY = "10d"
    RAIN_NIGHT = "10n"
    THUNDERSTORM_DAY = "11d"
    THUNDERSTORM_NIGHT = "11n"
    SNOW_DAY = "13d"
    SNOW_NIGHT = "13n"
    MIST_DAY = "50d"
    MIST_NIGHT = "50n"
    UNKNOWN = "unknown"

    @classmethod
    def parse_string(cls, string: str) -> Self:
        try:
            return cls(string)
        except ValueError:
            return cast(Self, cls.UNKNOWN)

class Weather_Forecast():
    time: datetime
    temperature: float
    feels_like: float
    desctiption: str
    icon: Weather_Icon

    def __init__ (self, open_weather_api_response: Dict) -> None:
        try:
            self.time = datetime.fromtimestamp(open_weather_api_response["dt"])
            self.temperature =  open_weather_api_response["main"]["temp"]
            self.feels_like = open_weather_api_response["main"]["feels_like"]
            self.description = open_weather_api_response["weather"][0]["description"]
            self.icon = Weather_Icon.parse_string(open_weather_api_response["weather"][0]["icon"])
        except Exception as e:
            raise ValueError(f"Invalid OpenWeather API response:") from e

    def to_dict(self) -> Dict:
        return {
            "time": self.time.isoformat(),
            "temperature": self.temperature,
            "feels_like": self.feels_like,
            "description": self.description,
            "icon": self.icon.value
        }

class City_Weather():
    city: str
    _cached_weather: List[Weather_Forecast]

    def __init__(self, city: str, display_name: str) -> None:
        self.city = city
        self.display_name = display_name
        self._cached_weather = []

    def cache_weather(self, cnt = 8) -> None:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={self.city}&appid={API_KEY}&units=metric&cnt={cnt}'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch weather data for {self.city}. Error code: {response.status_code}")
        
        try:
            weather_list = response.json()["list"]
            self._cached_weather = [Weather_Forecast(entry) for entry in weather_list]
        except Exception as e:
            raise ValueError(f"Could not parse OpenWeather API response for {self.city}") from e

    def get_weather(self) -> List[Weather_Forecast]:
        if not self._cached_weather:
            self.cache_weather()
        
        return self._cached_weather
    
    def get_weather_json(self) -> List[Dict]:
        weather = self.get_weather()
        return [weather_entry.to_dict() for weather_entry in weather]