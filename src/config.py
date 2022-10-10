import os
from dotenv import load_dotenv
from datetime import datetime
import logging

DATE_START = datetime.now()

class ColorLogFormatter(logging.Formatter):

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    green = '\033[32m'
    reset = '\x1b[0m'
    
    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.blue + self.fmt + self.reset,
            logging.INFO: self.green + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

PATH_DIR_LOGS = os.path.join(BASE_DIR, 'logs')

DEBUG = os.getenv('DEBUG') if os.getenv('DEBUG') is not None else 'False'
DEBUG = True if DEBUG =='True' else False

WS_BROKER_HOST = os.getenv('WS_BROKER_HOST') if os.getenv('WS_BROKER_HOST') is not None else 'localhost'
WS_BROKER_QUEUE = os.getenv('WS_BROKER_QUEUE') if os.getenv('WS_BROKER_QUEUE') is not None else 'ws_berezka'


TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
