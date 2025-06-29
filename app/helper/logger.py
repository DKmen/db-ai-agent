import logging
import os
from datetime import datetime

def setup_logger(log_file=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file is provided)
    if log_file:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = logging.FileHandler(f'logs/{log_file}_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# setup logger
logger = setup_logger('app')
