from weatherapi import fetch_data
import sqlite3 as sq
from datetime import datetime
from log_config import pipeline_logger

# input is hourly data from WeatherAPI, output is stored in database (hourly_data.db)
def store_hourly_data():
    data = fetch_data()
    
    if data is None:
        return False 

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
    hour = data['forecast']['forecastday'][0]['hour'][now_hour]
    row = make_hourly_row(hour)
    row = list(row)

    today = datetime.date(now)

    conn.execute("""INSERT OR IGNORE INTO hourly_data(time_epoch, time, temp_c, is_day, wind_kph, pressure_mb, precip_mm, humidity, dewpoint_c, will_it_rain, gust_kph) VALUES(?,?,?,?,?,?,?,?,?,?,?)""", row)

    # get the missing hours and storing them into the database (recovery)
    hours = get_missing_hours(str(today), now_hour)
    if hours:
         pipeline_logger.warning(f"Recovery triggered. Recovering {len(hours)} missing hour(s): {hours}")
    
    for i in hours:
        hour = data['forecast']['forecastday'][0]['hour'][i]
        row = make_hourly_row(hour)
        conn.execute("""INSERT OR IGNORE INTO hourly_data(time_epoch, time, temp_c, is_day, wind_kph, pressure_mb, precip_mm, humidity, dewpoint_c, will_it_rain, gust_kph) VALUES(?,?,?,?,?,?,?,?,?,?,?)""", row)
    
    if hours:
         pipeline_logger.info(f"Recovered {len(hours)} missing hour(s) successfully.")

    conn.commit()
    conn.close()
    
    return True


def get_missing_hours(today,now_hour):
    conn = sq.connect('data/hourly_data.db')  #---> makes it an independent function
    hours = []
    
    cursor = conn.execute("SELECT time FROM hourly_data WHERE time LIKE ?", (f"{today}%",))
    rows = cursor.fetchall()
    for i in range(0, now_hour+1, 1):
        found = False
        for row in rows:
            timestamp = row[0]
            hour = timestamp[11:13]
            hour = int(hour)
            #if hour == '0'+ str(i) or hour == str(i):   ------> this is for comparing strings
            if hour == i:   # here integers are compared so that '0' is not added to the hour
                found = True
                break
        if not found:
            hours.append(i)
   
    conn.close()

    return hours
    
def make_hourly_row(hour):
    return (
        hour['time_epoch'],
        hour['time'],
        hour['temp_c'],
        hour['is_day'],
        hour['wind_kph'],
        hour['pressure_mb'],
        hour['precip_mm'],
        hour['humidity'],
        hour['dewpoint_c'],
        hour['will_it_rain'],
        hour['gust_kph']
    )
    


