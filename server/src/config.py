# This file is a part of olympiade's server.
# It implements a singleton of config.
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013

class LogLevel:
    info = 0
    errors = 1
    warnings = 2
    debug = 3

class Config:
    port = 5000                  # Listen this port

    daemonize = False

    db_host = "localhost"
    db_user = "iu7_dbuser"
    db_pass = "krakazabra2k"
    db_name = "iu7_step"

    memcached_addr = "127.0.0.1:11211"
    session_timeout = 36000

    broadcast_listening_port = 27016
    broadcast_pause = 0.5

    ssl_enabled = False
    ssl_private_key = "ssl/cert.key"
    ssl_certificate = "ssl/cert.crt"

    log_level = LogLevel.debug
    stdout_logging = True                #won't work when in daemon mode
    log_file = "/var/log/iu7_step/main_log"

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(
                                 cls, *args, **kwargs)
        return cls._instance
