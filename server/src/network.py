# *-* coding: utf-8 *-*

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
        logger.Logger().debug(u"Сервер обрабатывает сообщение от клиента: %s" % self._buffer.decode('utf-8'));
        try:
            request = json.loads(self._buffer)
        except ValueError:
            logger.Logger().warn(u"Некорретный формат запроса пришел от клиента %s" % self.clientAddress)
            return request_not_valid_json()
        if not isinstance(request, dict):
            return request_not_valid_json()
        if request.get("id", None) is None:
            logger.Logger().warn(u"Не хватает параметра id от клиента %s" % self.clientAddress)
            return no_id_parametr()
        f_name = request.get("cmd", None)
        request["ip_addr"] = self.clientAddress
        if f_name is None or f_name not in api_functions:
            logger.Logger().warn(u"Неизвестная функция %s в запросе от клиента %s" % (f_name, self.clientAddress) )
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
            log.error(u"Произошла неизвестная ошибка: %s" % traceback.print_exc())
            result = unknown_error()
        self._buffer = ""
        error = result["error_code"]
        try:
            reply = json.dumps(result, ensure_ascii=False)
        except ValueError:
            log.error(u"Ошибка сериализации ответа сервера: %s" % traceback.print_exc())
            reply = '{"error_code": 0, "error_text": "Ошибка сереализации ответа"}'
            self.sendLine(reply)
            return

        self.sendLine(reply.encode('utf-8'))

        if error == 0:
            log.debug(u"Сервер послал ответ клиенту: [%s]" % reply)
        else:
            log.error(u"Сервер послал сообщение об ошибке клиенту: [%s]" % reply)

class ONPFactory(Factory):
    def buildProtocol(self, address):
        return ONP(address)

def broadcast_address():
    conf = Config()
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        cs.sendto("a", ('255.255.255.255', conf.broadcast_listening_port))
    except:
        cs.sendto("a", ('127.0.0.255', conf.broadcast_listening_port))
    cs.close()

def start_server():
    conf = Config()
    lc = LoopingCall(broadcast_address)
    lc.start(conf.broadcast_pause)
    factory = ONPFactory()
    if conf.ssl_enabled:
        reactor.listenSSL(conf.port, factory, ssl.DefaultOpenSSLContextFactory(conf.ssl_private_key, conf.ssl_certificate))
        logger.Logger().info(u"Сервер запустился в ssl-режиме на порту %d" % conf.port)
    else:
        reactor.listenTCP(conf.port, factory)
        logger.Logger().info(u"Сервер запустился на порту не-ssl-режиме на порту %d" % conf.port)
    reactor.run()
