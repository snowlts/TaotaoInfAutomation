import logging
import logging.config
import os
from datetime import  datetime

from config.config import get_path,config

LOG_LEVEL={
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

class Logger:
    def __init__(self,logger_name,console_log_level,file_log_level,logfile):
        self.logger_name = logger_name
        self.console_log_level=console_log_level
        self.file_log_level = file_log_level
        self.logfile = logfile

    def get_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            # create console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(self.console_log_level)
            # create file handler and set level to debug
            fh = logging.FileHandler(self.logfile)
            fh.setLevel(self.file_log_level)

            # create formatter
            FORMAT = "%(asctime)s-%(name)s-%(levelname)s-%(message)s"
            formatter = logging.Formatter(fmt=FORMAT)

            # add formatter to ch,fh
            ch.setFormatter(formatter)
            fh.setFormatter(formatter)

            # add ch.fh to logger
            logger.addHandler(ch)
            logger.addHandler(fh)
        return  logger

def logger_init(name=None):
    logger_name = name or config.log['logger_name']
    console_log_level =LOG_LEVEL[config.log['console_log_level']]
    file_log_level=LOG_LEVEL[config.log['file_log_level']]
    logfile_extention=config.log['logfile_extention']
    logfile= os.path.join(get_path("logs"),datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+logfile_extention)
    logger = Logger(logger_name,console_log_level,file_log_level,logfile).get_logger()
    return logger

def my_log(func):
    def wrapper(*args,**kw):
        print("=====start %s=================" % func.__name__)
        return func(*args,**kw)
    return wrapper

# logger = logger_init()
# # 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')
