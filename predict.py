from feature_eng import load_daily_data
from prediction import store_prediction
from log_config import pipeline_logger
from xgboost import XGBClassifier

def predict():
    data = load_daily_data()

    #running the ML model
    model = XGBClassifier()
    model.load_model("model/rain_classifier.json")

    feature_cols = ['temperature_min', 'temperature_max', 'temperature_mean', 'relative_humidity_min', 'relative_humidity_max', 'relative_humidity_mean', 'dewpoint_min',
    'dewpoint_max', 'dewpoint_mean', 'pressure_min', 'pressure_max', 'pressure_mean', 'wind_speed_mean', 'wind_gust_max', 'dT_mean', 'dH_mean', 'dP_mean', 'dayofyear',
    'month', 'rain_yesterday', 'rain_last3_days', 'pressure_3day_trend', 'humidity_3day_mean' ]

    #x_live= data[feature_cols]
    latest_day= data.iloc[[-1]]
    prediction = model.predict(latest_day[feature_cols])
    probability = model.predict_proba(latest_day[feature_cols])
    pipeline_logger.info(f"Prediction {prediction[0]}")
    pipeline_logger.info(f"Probability {probability[0][1]}")

    ans = store_prediction(prediction[0], probability[0][1])
    if not ans:
     return False


    if prediction[0] == 1:
         pipeline_logger.info("Carry an Umbrella")
    else:
         pipeline_logger.info("No Umbrella Required")
     
    return True

