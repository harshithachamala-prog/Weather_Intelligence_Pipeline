from weatherapi import fetch_data
import sqlite3 as sq
from datetime import datetime

def store_hourly_data():
    data = fetch_data()
    conn = sq.connect('data/hourly_data.db')
    conn.execute("""CREATE TABLE if not exists hourly_data(
                time_epoch INTEGER,
                time TEXT PRIMARY KEY,
                temp_c REAL,
                is_day INTEGER,
                wind_kph REAL,
                pressure_mb REAL,
                precip_mm REAL,
                humidity INTEGER,
                dewpoint_c REAL,
                will_it_rain INTEGER,
                gust_kph REAL);
            """)
    
    
    now = datetime.now()
    
    """ #this is the code that will be used if WeatherAPI data is not indexed properly
    for i in range (24):
        row =  data['forecast']['forecastday'][0]['hour'][i]
        print('the time of the row : ', row)
        dt_obj = datetime.strptime(row['time'] , "%Y-%m-%d %H:%M")
        print(now.hour)
        print(dt_obj.hour)
    """
    now_hour = now.hour
    #row =  data['forecast']['forecastday'][0]['hour'][now_hour]
    row = data['forecast']['forecastday'][0]['hour'][now_hour].values()
    row = list(row)
    conn.execute("""INSERT INTO hourly_data VALUES(?,?,?,?,?,?,?,?,?,?,?)""", row)
    
    conn.commit()
    conn.close()



