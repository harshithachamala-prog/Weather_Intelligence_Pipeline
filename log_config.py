import logging 
import os

def create_logger(name, filename):
    os.makedirs('logs', exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)


    if not logger.handlers:
        
        file_handler = logging.FileHandler(f"logs/{filename}.log")
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

pipeline_logger = create_logger("pipeline", "pipeline")
scheduler_logger = create_logger("scheduler", "scheduler")
api_logger = create_logger("api", "api")
error_logger = create_logger("error", "error")

