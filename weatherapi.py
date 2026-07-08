import requests
from log_config import pipeline_logger



def fetch_data():
    try: 
         response = requests.get("http://api.weatherapi.com/v1/forecast.json", params={"key" : "--", "q": "Bangalore", "days": "3"} )
         response.raise_for_status()
         data = response.json()
         return data
    except Exception as e:
        pipeline_logger.error(f"Failed to fetch data from WeatherAPI: {e}")
        return None


