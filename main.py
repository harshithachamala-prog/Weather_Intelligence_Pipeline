from database import store_hourly_data
#from datetime import datetime
from feature_eng import save_daily
from predict import predict
import time
from log_config import pipeline_logger
#from weatherapi import fetch_data

def retry(func, retries=3, delay=120):
    for i in range(retries):
        if func():
            return True
        time.sleep(delay)
    return False


def main():
    #print("main executed at:", datetime.now())
    pipeline_logger.info("Pipelineexecution started")
    if retry(store_hourly_data) :
       pipeline_logger.info("Hourly data stored successfully.")
       if retry(save_daily) :
             pipeline_logger.info("Daily data stored successfully.")
             if retry(predict) :
                 pipeline_logger.info("Prediction has been made successfully.")
                 pipeline_logger.info("Pipeline execution completed.")
             else:
                 pipeline_logger.error("Failed to make prediction after multiple attempts.")
       else:
        pipeline_logger.error("Failed to store daily data after multiple attempts.")
    else:
        pipeline_logger.error("Failed to store hourly data after multiple attempts.")
    


        




