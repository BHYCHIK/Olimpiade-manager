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
import logger
import json
import traceback

# ONP - Olympiade network protocol
class ONP(LineReceiver):
    def __init__(self, address):
        self.clientAddress = address
        self._buffer = ""
        self._json_state = 0 # is opened - closed figure brackets

    def operate(self):
        logger.Logger().debug("Proccessing message: %s" % self._buffer);
        try:
            request = json.loads(self._buffer)
        except ValueError:
            logger.Logger().warn("Invalid json came from %s" % self.clientAddress)
            return request_not_valid_json()
        if not isinstance(request, dict):
            return request_not_valid_json()
        if request.get("id", None) is None:
            logger.Logger().warn("No id parametr from %s" % self.clientAddress)
            return no_id_parametr()
        f_name = request.get("cmd", None)
        request["ip_addr"] = self.clientAddress
        if f_name is None or f_name not in api_functions:
            logger.Logger().warn("Unkown api function %s in request from %s" % (f_name, self.clientAddress) )
            return unknown_api_function(request)
        return api_functions[f_name](request)

    def lineReceived(self, line):
        self._buffer = self._buffer + "\r\n" + line
        self._json_state = self._json_state + sum(1 for i in line if i == '{') - sum(1 for i in line if i == '}')
        if self._json_state == 0:
            try:
                reply = self.operate()
            except Exception:
                logger.Logger().error("UNKNOWN ERROR HAPPENED: %s" % traceback.print_exc())
                reply = unknown_error()
            self._buffer = ""
            if reply != None:
                self.sendLine(reply)

class ONPFactory(Factory):
    def buildProtocol(self, address):
        return ONP(address)

def start_server():
    conf = Config()
    factory = ONPFactory()
    if conf.ssl_enabled:
        reactor.listenSSL(conf.port, factory, ssl.DefaultOpenSSLContextFactory(conf.ssl_private_key, conf.ssl_certificate))
        logger.Logger().info("Server started in ssl mode on port %d" % conf.port)
    else:
        reactor.listenTCP(conf.port, factory)
        logger.Logger().info("Server started in non-ssl mode on port %d" % conf.port)
    reactor.run()
