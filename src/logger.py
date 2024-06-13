import logging
from logging.handlers import TimedRotatingFileHandler

from src.globalconfig import GlobalConfig
from src.types import InternalError
from src.types.errorcode import *


class Logger(object):
    __instance = None

    def __init__(self):
        if Logger.__instance is not None:
            raise InternalError(ERROR_COMMON_0001)

        logConfig = GlobalConfig.instance().LOG
        logDir = logConfig['LOG_DIR'] if 'LOG_DIR' in logConfig else 'logs'
        fileName = logConfig['FILE_NAME'] if 'FILE_NAME' in logConfig else 'log_file.log'
        when = logConfig['WHEN'] if 'WHEN' in logConfig else 'midnight'
        interval = int(logConfig['INTERVAL']) if 'INTERVAL' in logConfig else 1
        backupCount = int(logConfig['BACKUP_COUNT']) \
            if 'BACKUP_COUNT' in logConfig else 7

        # Split log at 0h everyday
        handler = TimedRotatingFileHandler(f'./{logDir}/{fileName}',
                                           when=when,
                                           interval=interval,
                                           backupCount=backupCount)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.__logger = logging.getLogger('RotatingFileHandler')
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.addHandler(handler)
        Logger.__instance = self

    @staticmethod
    def instance():
        """ Static access method. """
        if Logger.__instance is None:
            Logger()
        return Logger.__instance

    def debug(self, content):
        self.__logger.debug(content)

    def info(self, content):
        self.__logger.info(content)

    def warning(self, content):
        self.__logger.warning(content)

    def error(self, content):
        self.__logger.error(content)

    def critical(self, content):
        self.__logger.critical(content)
