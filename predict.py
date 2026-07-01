from feature_eng import load_daily_data
from xgboost import XGBClassifier

def predict():
    data = load_daily_data()
    print(data.columns.tolist())
    print(data.shape)
    print(data.head())

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
    print("Prediction", prediction[0])
    print("Probability", probability[0][1])

    if prediction[0] == 1:
         print("Carry an Umbrella")
    else:
         print("No Umbrella Required")
     
    return True

