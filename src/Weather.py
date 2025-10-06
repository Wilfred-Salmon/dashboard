import dotenv
import os
import requests
from typing import Dict

dotenv.load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

class Weather():
    city: str
    _cached_weather: Dict

    def __init__(self, city: str) -> None:
        self.city = city

    def cache_weather(self, cnt = 8) -> None:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={self.city}&appid={API_KEY}&units=metric&cnt={cnt}'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch weather data for {self.city}. Error code: {response.status_code}")
        
        self._cached_weather = response.json()["list"]

    def get_weather(self) -> Dict:
        if not self._cached_weather:
            self.cache_weather()
        
        return self._cached_weather