import logging
from decouple import config

DEBUG = config("DEBUG", cast=bool, default=False)

logging_level = logging.INFO
if DEBUG:
    logging_level = logging.DEBUG
logging.basicConfig(level=logging_level, format='[%(levelname)s: %(asctime)s] %(name)s - %(message)s')
