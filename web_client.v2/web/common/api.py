import datetime
import time
import settings
import socket
import json

class ApiUser(object):
    def __init__(self, request):
        if 'id' in request.session:
            session_id = request.session['id']
            self._session_id = session_id
            api = Api(session_id)
            self._is_authenticated = api.check_session()
            print('User is %sauthenticated' % ('' if self._is_authenticated else 'NOT '))
        else:
            self._is_authenticated = False
            print('user is not authenticated')
    def login(self, request, login, password):
        session_id = Api().account_login({'login': login, 'password': password})
        if session_id:
            print('valid login')
            request.session['id'] = session_id
        else:
            print('invalid login')
        return session_id

    def logout(self):
        return Api(self._session_id).logout()
    def is_authenticated(self):
        print('return %s' % ('true' if self._is_authenticated else 'false'))
        return self._is_authenticated

class Api(object):
    ERR_CODE_OK = 0

    def __init__(self, session_id=None):
        self._session_id = session_id

    def _send_req(self, cmd, data):
        json_data = dict(data)
        json_data.update({'id': 1, 'cmd': cmd, 'ip_addr': '127.0.0.1', 'session_id': self._session_id})
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

    def register_person(self, reg_data):
        data = {}
        for key, value in reg_data.iteritems():
            if isinstance(value, datetime.date):
                data[key] = time.strftime('%Y-%m-%d', value.timetuple())
            else:
                data[key] = value if value is not None else '' # hack because API doesn't support null values or missing fields
        return self._send_req('onp_register_person', data)

    def register_account(self, reg_data):
        return self._send_req('onp_register_account', reg_data)

    def account_login(self, login_data):
        res = self._send_req('onp_request_session', login_data)
        print(res)
        return res['session_id'] if res else None

    def get_all_persons(self):
        MAX_PERSONS = 1000
        req = {'from': 0, 'count': MAX_PERSONS}
        res = self._send_req('onp_get_people', req)
        print(res)
        return res['data']

    def check_session(self):
        return self._send_req('onp_check_session', {})

    def logout(self):
        return self._send_req('onp_logout', {})
