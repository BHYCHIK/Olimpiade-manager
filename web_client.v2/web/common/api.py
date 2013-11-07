import datetime
import time
import settings
import socket
import json
from django.shortcuts import render_to_response
from django.template import RequestContext

class ApiUser(object):
    def __init__(self, request):
        if 'id' in request.session:
            session_id = request.session['id']
            self._session_id = session_id
            api = Api(session_id)
            self._is_authenticated = api.check_session()
        else:
            self._is_authenticated = False
        print('[%s]: is authenticated = %s' % (request.path, str(self._is_authenticated)))
    def login(self, request, login, password):
        session_id = Api().account_login({'login': login, 'password': password})
        if session_id:
            request.session['id'] = session_id
        return session_id

    def logout(self):
        return Api(self._session_id).logout()
    def is_authenticated(self):
        return self._is_authenticated

    @staticmethod
    def login_required(func):
        def wrapper(request, *args , **kwargs):
            if request.api_user.is_authenticated():
                return func(request, *args, **kwargs)
            return render_to_response('common/no_access.html',
                                      context_instance=RequestContext(request))
        return wrapper


class Api(object):
    ERR_CODE_OK = 0

    def __init__(self, session_id=None):
        self._session_id = session_id

    def _send_req(self, cmd, data):
        json_data = dict(data)
        json_data.update({'id': 1, 'cmd': cmd, 'ip_addr': '127.0.0.1', 'session_id': self._session_id})
        print('[%s]: frontend is trying to send %s to backend' % (cmd, json.dumps(json_data)))
        try:
            sock = socket.create_connection(settings.BACKEND_HOST, settings.BACKEND_TIMEOUT)
            sock.send(json.dumps(json_data) + '\r\n')
            data = ' '
            response = ''
            while len(data):
                data = sock.recv(4096)
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

        print('[%s]: frontend got from backend: %s' % (cmd, response))
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
        return res['session_id'] if res else None

    def get_all_persons(self):
        MAX_PERSONS = 1000
        req = {'from': 0, 'count': MAX_PERSONS}
        res = self._send_req('onp_get_people', req)
        return res['data'] if res and 'data' in res else None 

    def check_session(self):
        return self._send_req('onp_check_session', {})

    def logout(self):
        return self._send_req('onp_logout', {})
