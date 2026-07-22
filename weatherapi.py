import requests
import os
from log_config import pipeline_logger
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def fetch_data():
    try: 
         response = requests.get("http://api.weatherapi.com/v1/forecast.json", params={"key" : API_KEY, "q": "Bangalore", "days": "3"} )
         response.raise_for_status()
         data = response.json()
         return data
    except Exception as e:
        pipeline_logger.error(f"Failed to fetch data from WeatherAPI: {e}")
        return None


