
import logging
from src.config import ColorLogFormatter, PATH_DIR_LOGS, DATE_START, DEBUG
import os

logger = logging.getLogger('tg-berezka')
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
c_format = ColorLogFormatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

f_handler = logging.FileHandler(os.path.join(PATH_DIR_LOGS, f'tg-berezka-{DATE_START}.log'))
f_format = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
f_handler.setFormatter(f_format)
f_handler.setLevel(logging.DEBUG)
logger.addHandler(f_handler)

if DEBUG:
    c_handler.setLevel(logging.DEBUG)
else:
    c_handler.setLevel(logging.INFO)

from src.tg import start_tg_client

if __name__ == '__main__':
    try:
        logger.info('Запуск Telegram клиента')
        start_tg_client()
    except Exception as ex:
        logger.exception(ex)    