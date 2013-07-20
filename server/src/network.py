# This file is a part of olympiade's server.
# It implements a networking part
# It must not interpretated data, only tries to understand when json is finished.
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import ssl, reactor
from config import Config
from error_handlers import *
from onp_api import *
import json

# ONP - Olympiade network protocol
class ONP(LineReceiver):
    def __init__(self, address):
        self.clientAddress = address
        self._buffer = ""
        self._json_state = 0 # is opened - closed figure brackets

    def operate(self):
        try:
            request = json.loads(self._buffer)
        except ValueError:
            return request_not_json()
        f_name = request.get("cmd", None)
        if f_name is None or f_name not in api_functions:
			return unknown_api_function()
        return api_functions[f_name](request)

    def lineReceived(self, line):
		print "Success!"
		print line;
		self._buffer = self._buffer + "\r\n" + line
		self._json_state = self._json_state + sum(1 for i in line if i == '{') - sum(1 for i in line if i == '}')
		if self._json_state == 0:
			reply = self.operate()
			self._buffer = ""
			if reply != None:
				self.sendLine(reply)

class ONPFactory(Factory):
    def buildProtocol(self, address):
        return ONP(address)

def start_server():
    config = Config()
    factory = ONPFactory()
    if config.ssl_enabled:
	    reactor.listenSSL(config.port, factory, ssl.DefaultOpenSSLContextFactory(config.ssl_private_key, config.ssl_certificate))
    else:
        reactor.listenTCP(config.port, factory)
    reactor.run()
