# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/14 16:54
@File: logHepler.py
@Project: Proxy-Pool
@Description: None
"""


import os
import logging
from logging.handlers import TimedRotatingFileHandler

# 日志级别，拷贝自logging库
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')

if not os.path.exists(LOG_PATH):
    try:
        os.mkdir(LOG_PATH)
    except FileExistsError:
        pass


class LogHelper(logging.Logger):

    def __init__(self, name, level=INFO,
                 formatter="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s"):
        super(LogHelper, self).__init__(name=name, level=level)
        self.format = formatter
        self.__setFileHandler__()
        self.__setStreamHandler__()

    def __setFileHandler__(self):
        file_name = os.path.join(LOG_PATH, '{}.log'.format(self.name))
        file_handler = TimedRotatingFileHandler(filename=file_name, when='H',
                                                interval=3, backupCount=10)
        # file_handler.suffix = "%Y-%m-%d.log"
        formatter = logging.Formatter(self.format)
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

    def __setStreamHandler__(self):
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(self.format)
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)


if __name__ == '__main__':
    log = LogHelper("test")
    log.info("test")
    log.debug("debug")
    log.error("error")
