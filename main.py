from database import store_hourly_data
from datetime import datetime
from feature_eng import save_daily
from predict import predict
import time
#from weatherapi import fetch_data

def retry(func, retries=3, delay=120):
    for i in range(retries):
        if func():
            return True
        time.sleep(delay)
    return False


def main():
    #print("main executed at:", datetime.now())
    if retry(store_hourly_data) :
       print("Hourly data stored successfully.")
       if retry(save_daily) :
             print("Daily data stored successfully.")
             if retry(predict) :
                 print("Prediction has been made successfully.")
             else:
                 print("Failed to make prediction after multiple attempts.")
       else:
        print("Failed to store daily data after multiple attempts.")
    else:
        print("Failed to store hourly data after multiple attempts.")


        




