import pandas as pd 
import numpy as numpy
import sqlite3 as sq 

conn = sq.connect('data/hourly_data.db')

df =  pd.read_sql_query("SELECT * FROM hourly_data", conn)
conn.close()
print(df.head())
print(df.shape)
print(df.dtypes)

#calulating dT, dH, dP
df["temp_lag"] = df['temp_c'].shift(1)
df['humidity_lag'] = df['humidity'].shift(1)
df['pressure_lag'] = df['pressure_mb'].shift(1)
df['dT'] = df['temp_c'] - df['temp_lag']
df['dH'] = df['humidity'] - df['humidity_lag']
df['dP'] = df['pressure_mb'] - df['pressure_lag']

df["time"] = pd.to_datetime(df["time"], errors="coerce", utc=True)
df["date"] = df["time"].dt.floor("D")  

df = df.drop(columns=['temp_lag', 'humidity_lag', 'pressure_lag', 'time_epoch', 'time'])

daily = df.groupby('date').agg({ 
    "temp_c": ["min", "max", "mean"],
    "humidity": ["min", "max", "mean"],
    "dewpoint_c": ["min", "max", "mean"],
    "pressure_mb": ["min", "max", "mean"],
    "wind_kph": ["mean"],
    "gust_kph": ["max"],
    "precip_mm": ["sum"],  
    "dT": ["mean"],
    "dH": ["mean"],
    "dP": ["mean"],

})

daily["dayofyear"] = daily.index.dayofyear
daily["month"] = daily.index.month
print(daily.head())
print(daily.shape)
print(daily.columns)

#To flatten the multiindexed columns
daily.columns = ["_".join(col).strip() for col in daily.columns]
print(daily.columns.tolist())

#to rename the columns
daily.rename(columns={ 'temp_c_min': 'temperature_min','temp_c_max': 'temperature_max', 'temp_c_mean': 'temperature_mean'}, inplace=True)
daily.rename(columns={ 'humidity_min' : 'relative_humidity_min', 'humidity_max' : 'relative_humidity_max', 'humidity_mean' : 'relative_humidity_mean'}, inplace=True)
daily.rename(columns={ 'dewpoint_c_min' : 'dewpoint_min', 'dewpoint_c_max' : 'dewpoint_max', 'dewpoint_c_mean' : 'dewpoint_mean' }, inplace=True)
daily.rename(columns={ 'pressure_mb_min' : 'pressure_min', 'pressure_mb_max' : 'pressure_max', 'pressure_mb_mean' : 'pressure_mean' }, inplace = True)
daily.rename(columns={ 'wind_kph_mean' : 'wind_speed_mean', 'gust_kph_max' : 'wind_gust_max'}, inplace = True)
daily.rename(columns={ 'dayofyear_' : 'dayofyear', 'month_': 'month'}, inplace = True)
daily.rename(columns={ 'precip_mm_sum' : 'rain_mm'}, inplace = True)
print(daily.columns.tolist())

#adding the missing proxy columns
daily['rain_yesterday'] = 0
daily['rain_last3_days'] = daily['rain_mm']
daily['pressure_3day_trend'] = 0
daily['humidity_3day_mean'] = daily['relative_humidity_mean']
print(daily.columns.tolist())

