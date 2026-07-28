from database import store_hourly_data
#from datetime import datetime
from feature_eng import save_daily
from predict import predict
import time
from log_config import pipeline_logger
#from weatherapi import fetch_data

def retry(func, retries=3, delay=120):
    for i in range(retries):
        try:
            if func():
                return True

        except Exception as e:
            pipeline_logger.error(
                f"{func.__name__} failed on attempt {i + 1}: {e}")

        if i < retries - 1:
            time.sleep(delay)

    return False


def main():
    #print("main executed at:", datetime.now())
    pipeline_logger.info("Pipeline execution started")
    if not retry(store_hourly_data) :
        pipeline_logger.error("Failed to store hourly data after multiple attempts.")
        raise RuntimeError("Hourly data has not been stored successfully.")
    
    pipeline_logger.info("Hourly data stored successfully.")
       
    if not retry(save_daily) :
        pipeline_logger.error("Failed to store daily data after multiple attempts.")
        raise RuntimeError("Daily data processing failed")
    
    pipeline_logger.info("Daily data stored successfully.")
             
    if not retry(predict) :
        pipeline_logger.error("Failed to make prediction after multiple attempts.")
        raise RuntimeError("Prediction failed")
    
    pipeline_logger.info("Prediction has been made successfully.")
    pipeline_logger.info("Pipeline execution completed.")
      
    return True
        
