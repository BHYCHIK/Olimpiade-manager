# This file is a part of olympiade's server.
# It implements a singleton of config.
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013

class Config:
	listen_address = "0.0.0.0"    # Listen this address.
	port = 27017                  # Listen this port
	
	_instance = None
	def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance	
