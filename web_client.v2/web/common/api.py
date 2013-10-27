import datetime
import time
import settings
import socket
import json

class Api(object):
    ERR_CODE_OK = 0

    def _send_req(self, cmd, data):
        json_data = dict(data)
        json_data.update({'id': 1, 'cmd': cmd})
        try:
            sock = socket.create_connection(settings.BACKEND_HOST, settings.BACKEND_TIMEOUT)
            sock.send(json.dumps(json_data) + '\r\n')
            data = ' '
            response = ''
            while len(data):
                data = sock.recv(4096)
                print('received ' + data)
                response += data
                error = False
                try:
                    result = json.loads(response)
                except ValueError:
                    error = True
                if not error:
                    break

        except socket.error as ex:
            print('Socket error')
            print(ex)
            return None

        if result['error_code'] != self.ERR_CODE_OK:
            print('got error')
            return None

        return result

    def register_person(self, reg_form):
        data = {}
        for key, value in reg_form.cleaned_data.iteritems():
            if isinstance(value, datetime.date):
                data[key] = time.strftime('%d/%m.%Y', value.timetuple())
            else:
                data[key] = value if value is not None else '' # hack because API doesn't support null values or missing fields
        res = self._send_req('onp_register_person', data)
        print(res)
        return True
