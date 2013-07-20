# This file is a part of olympiade's server.
# It implements a singleton of config.
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013

class Config:
    port = 5000                  # Listen this port

    ssl_enabled = False
    ssl_private_key = "ssl/cert.key"
    ssl_certificate = "ssl/cert.crt"
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(
                                 cls, *args, **kwargs)
        return cls._instance	
