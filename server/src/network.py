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
import StringIO
import struct

class Iproto:
    def __init__(self):
        _sync = 0

    class TypeToIprotoCodes:
        dict_type = 1
        string_type = 2
        list_type = 3
        int_type = 4
        float_type = 5
        none_type = 6

    def iproto_serialize(self, data):
        if isinstance(data, dict):
            return self._iproto_serialize_dict(data)
        elif isinstance(data, int):
            return self._iproto_serialize_int(data)
        elif isinstance(data, float):
            return self._iproto_serialize_float(data)
        elif isinstance(data, str):
            return self._iproto_serialize_string(data)
        elif isinstance(data, list) or isinstance(data, tuple):
            return self._iproto_serialize_list(data)
        elif isinstance(data, int):
            return self._iproto_serialize_int(data)
        elif isinstance(data, bool):
            return self._iproto_serialize_bool(data)
        elif data is None:
            return self._iproto_serialize_none()

    def _iproto_serialize_dict(self, data):
        serialized = struct.pack("!BQ", self.TypeToIprotoCodes.dict_type, len(data))
        for key in data:
            serialized = serialized + self.iproto_serialize(key) + self.iproto_serialize(key)
        return serialized

    def _iproto_serialize_int(self, data):
        serialized = struct.pack("!Bq", self.TypeToIprotoCodes.int_type, data)
        return serialized

    def _iproto_serialize_none(self):
        serialized = struct.pack("!B", self.TypeToIprotoCodes.none_type)
        return serialized

    def _iproto_serialize_bool(self, data):
        serialized = struct.pack("!B?", self.TypeToIprotoCodes.int_type, data)
        return serialized

    def _iproto_serialize_float(self, data):
        serialized = struct.pack("!Bd", self.TypeToIprotoCodes.int_type, data)
        return serialized

    def _iproto_serialize_string(self, data):
        str_len = len(data)
        serialized = struct.pack("!BB%ss" % str_len, TypeToIprotoCodes.int_type, str_len, data)
        return serialized

    def _iproto_serialize_list(self, data):
        serialized = struct.pack("!BQ", TypeToIprotoCodes.dict_type, len(data))
        for element in data:
            serialized = serialized + self._iproto_serialize(element)
        return serialized

    def iproto_uniform_packet(self, data):
        body = iproto_serialize(data);
        header = struct.pack("!ii", sync, len(body))
        if self._sync == (2 ** 32 - 1):
            self._sync = 0
        else:
            self._sync = self._sync + 1
        return header + body

# ONP - Olympiade network protocol
class ONP(LineReceiver):
    def __init__(self, address):
        self.clientAddress = address
        self._buffer = ""
        self._json_state = 0 # is opened - closed figure brackets
        self._iproto_maker = Iproto()

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
