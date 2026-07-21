import sqlite3 as sq
from log_config import pipeline_logger
from log_config import api_logger

def store_prediction(pred, prob):
    data = None
    try:
        data = sq.connect("data/prediction.db")
        data.execute("""CREATE TABLE IF NOT EXISTS prediction(
        date text primary key,
        prediction integer,
        probability real);""")

        temp = (pred, prob)
        data.execute("INSERT OR REPLACE INTO prediction VALUES(DATE('now'),?,?)", temp) #if better prediction found then value changes
        data.commit()
        return True
    except Exception as e:
        pipeline_logger.error(f"Failed to commit data to prediction.db: {e}")
        return False
    finally:
        if data is not None:
             data.close()

    

def get_prediction():
    data = None
    try:
        data = sq.connect("data/prediction.db")
        cursor = data.execute("SELECT * FROM prediction WHERE DATE = DATE('now')")
        row = cursor.fetchone()
        if row is not None:
            d = {'date' : row[0], 'prediction' : row[1], 'probability': row[2]}
            return d
        else:
            return None
    except Exception as e:
        api_logger.error(f"Failed to retrieve data from prediction.db: {e}")
        return None
    finally:
        if data is not None:
             data.close()

    
    




