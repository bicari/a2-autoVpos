import logging
from logging.handlers import TimedRotatingFileHandler


def logger():
    log = logging.getLogger('logger_vpos')
    log.setLevel(logging.INFO)
    if log.hasHandlers():
        log.handlers.clear()
    formatter = logging.Formatter('%(asctime)s %(levelname)s : %(message)s')
    file_handler = TimedRotatingFileHandler(
                                'logs\\logs_data.log',
                                when='midnight',
                                backupCount=7,
                                encoding='utf-8'
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    log.addHandler(console_handler)

    #def info (message):
    return log

