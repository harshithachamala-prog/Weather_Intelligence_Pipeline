from pydantic import BaseModel
# used to define the blueprint of the FastAPI
class Prediction(BaseModel):
    date : str
    prediction : int
    probability : float


class DailyWeather(BaseModel):
    date: str
    temperature_min: float
    temperature_max: float
    temperature_mean: float

    relative_humidity_min: float
    relative_humidity_max: float
    relative_humidity_mean: float

    dewpoint_min: float
    dewpoint_max: float
    dewpoint_mean: float

    pressure_min: float
    pressure_max: float
    pressure_mean: float

    wind_speed_mean: float
    wind_gust_max: float

    rain_mm: float

    dT_mean: float
    dH_mean: float
    dP_mean: float

    dayofyear: int
    month: int

    rain_yesterday: float
    rain_last3_days: float

    pressure_3day_trend: float
    humidity_3day_mean: float

class ApiHealth(BaseModel):
    status : str
    daily_database : str 
    model : str
    prediction_database : str
