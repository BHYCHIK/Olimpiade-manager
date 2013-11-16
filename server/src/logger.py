# *-* coding: utf-8 *-*

# This file is a part of olympiade's server.
# It implements a singleton of logger.
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013

import config
import time
import os
import threading

class Logger:
    _instance = None
    _mutex = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(
                                 cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        conf = config.Config()
        log_file_dir = os.path.dirname(conf.log_file)
        self._mutex = threading.Lock()
        self._mutex.acquire()
        if not os.path.isdir(log_file_dir):
            os.makedirs(log_file_dir)
        self._mutex.release()

    def debug(self, message):
        conf = config.Config()
        if conf.log_level >= config.LogLevel.debug:
            self._real_logging(u"Отладочная информация", message)

    def warn(self, message):
        conf = config.Config()
        if conf.log_level >= config.LogLevel.warnings:
            self._real_logging(u"Предупреждение", message)

    def error(self, message):
        conf = config.Config()
        if conf.log_level >= config.LogLevel.errors:
            self._real_logging(u"Ошибка", message)

    def info(self, message):
        conf = config.Config()
        if conf.log_level >= config.LogLevel.info:
            self._real_logging(u"Информация", message)

    def _real_logging(self, level, message):
        conf = config.Config()
        self._mutex.acquire()
        log_file = open(conf.log_file, "at");
        msg = u"СЕРВЕР [" + time.ctime() + "] " + message
        log_file.write(msg)
        log_file.close()

        if not conf.daemonize and conf.stdout_logging:
            print u"[%s] at [%s]: %s" % (level, time.ctime(), message)
        self._mutex.release()

