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
from twisted.internet.task import LoopingCall
import logger
import json
import traceback
import StringIO
import struct
import threading
import time
import socket
import sys

# ONP - Olympiade network protocol
class ONP(LineReceiver):
    def __init__(self, address):
        self.clientAddress = address
        self._buffer = ""
        self._json_state = 0 # is opened - closed figure brackets

    def operate(self):
        logger.Logger().debug("Processing message: %s" % self._buffer);
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
        result = api_functions[f_name](request)
        return result

    def lineReceived(self, line):
        self._buffer = self._buffer + "\r\n" + line
        self._json_state = self._json_state + sum(1 for i in line if i == '{') - sum(1 for i in line if i == '}')
        if self._json_state != 0:
            return
        log = logger.Logger()
        try:
            result = self.operate()
        except Exception:
            log.error("UNKNOWN ERROR HAPPENED: %s" % traceback.print_exc())
            result = unknown_error()
        self._buffer = ""
        error = result["error_code"]
        try:
            reply = json.dumps(result)
        except ValueError:
            log.error("Error of serializing result to JSON: %s" % traceback.print_exc())
            reply = '{"error_code": 0, "error_text": "serializing to JSON error"}'
            self.sendLine(reply)
            return

        self.sendLine(reply)

        if error == 0:
            log.debug("Server sent response to client: [%s]" % reply)
        else:
            log.error("Server sent error to client: [%s]" % reply)

class ONPFactory(Factory):
    def buildProtocol(self, address):
        return ONP(address)

def broadcast_address():
    conf = Config()
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    logger.Logger().info("Sending: %s" % broadcast_data)
    cs.sendto("a", ('255.255.255.255', conf.broadcast_listening_port))
    cs.close()

def start_server():
    conf = Config()
    lc = LoopingCall(broadcast_address)
    lc.start(conf.broadcast_pause)
    factory = ONPFactory()
    if conf.ssl_enabled:
        reactor.listenSSL(conf.port, factory, ssl.DefaultOpenSSLContextFactory(conf.ssl_private_key, conf.ssl_certificate))
        logger.Logger().info("Server started in ssl mode on port %d" % conf.port)
    else:
        reactor.listenTCP(conf.port, factory)
        logger.Logger().info("Server started in non-ssl mode on port %d" % conf.port)
    reactor.run()
