from fastapi import FastAPI, HTTPException 
from prediction import get_prediction
from Pydantic_schema import Prediction, DailyWeather, ApiHealth
from feature_eng import load_daily_data
import os
#import pandas as pd


app = FastAPI(title = 'Weather Intelligence Pipeline API', description = 'REST API for an automated weather prediction pipeline. The service collects hourly weather data, performs feature engineering, runs an XGBoost rainfall prediction model, and exposes the latest weather metrics and predictions through FastAPI.', version = '1.0.0')

@app.get("/", tags = ['System'])
def root():
    return {'Status' : 'API is running' }

@app.get("/prediction", tags = ['Prediction'], summary = 'Gets the latest prediction', description = 'Returns the prediction made for the given date', response_model = Prediction)
def prediction_api():
    row = get_prediction()
    if row is not None:
        return row
    raise HTTPException(status_code= 404, detail = "No prediction available")

@app.get("/daily", tags = ['Weather'], summary = 'Gets the latest engineered weather data', description = 'Returns the latest daily engineered weather features used by the prediction model.', response_model = DailyWeather)
def get_daily_data_api():
    data= load_daily_data()
    if data.empty:
        raise HTTPException(status_code = 404, detail = "No daily Weather data available")
    latest = data.iloc[-1]
    return latest.to_dict()

@app.get("/health",tags = ['System'], summary = 'Gets health status of pipeline', description = 'Returns the latest health status of the data pipeline ', response_model = ApiHealth)
def health_display():
    health = {}
    count = 0
    if os.path.exists('data/daily_data.db'):
        health['daily_database'] = 'Connected'
        count = count + 1
    else:
        health['daily_database'] = 'Missing'

    if os.path.exists('model/rain_classifier.json'):
        health['model'] = 'Loaded'
        count = count + 1
    else:
       health['model'] = 'Missing'

    if os.path.exists("data/prediction.db"):
        health['prediction_database'] = 'Connected'
        count = count + 1
    else:
        health['prediction_database'] = 'Missing'
    if count == 3:
         health['status'] = 'Healthy'
    else:
        health['status'] = 'Degraded'

    return health



     

    