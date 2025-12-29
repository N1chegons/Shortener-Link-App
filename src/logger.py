import logging
import sys
from datetime import datetime


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ],
        force=True
    )

def get_logger(name):
    return logging.getLogger(name)

setup_logging()
logger = get_logger(__name__)