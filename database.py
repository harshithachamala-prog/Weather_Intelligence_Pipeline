from main import data
import sqlite3 as sq
 
conn = sq.connect('data/hourly_data.db')
cursor = conn.cursor()
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
for i in range (1,24):
    row =  data['forecast']['forecastday'][0]['hour'][i].values()
    print('the value of a row : ', row)
    row = list(row)
    conn.execute("""INSERT INTO hourly_data VALUES(?,?,?,?,?,?,?,?,?,?,?)""", row)
conn.commit()
conn.close()
