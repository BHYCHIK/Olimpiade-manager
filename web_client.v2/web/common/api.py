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
            self._is_admin = True if request.session['admin_priv'] else False
        else:
            self._is_authenticated = False
        print('[%s]: is authenticated = %s' % (request.path, str(self._is_authenticated)))
    def login(self, request, login, password):
        session_id, admin_priv = Api().account_login({'login': login, 'password': password})
        if session_id:
            request.session['id'] = session_id
            request.session['admin_priv'] = admin_priv
        return session_id

    def logout(self):
        return Api(self._session_id).logout()
    def is_authenticated(self):
        return self._is_authenticated
    def is_admin(self):
        return self.is_authenticated() and self._is_admin

    @staticmethod
    def login_required(func):
        def wrapper(request, *args, **kwargs):
            if request.api_user.is_authenticated():
                api = Api(request.session['id'])
                return func(request, api, *args, **kwargs)
            return render_to_response('common/no_access.html',
                                      context_instance=RequestContext(request))
        return wrapper

    @staticmethod
    def admin_required(func):
        def wrapper(request, *args, **kwargs):
            if request.api_user.is_admin():
                api = Api(request.session['id'])
                return func(request, api, *args, **kwargs)
            return render_to_response('common/no_access.html',
                                      context_instance=RequestContext(request))
        return wrapper


class Api(object):
    ERR_CODE_OK = 0
    MAX_ELEMENTS = 1000

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
        return (res['session_id'], res['admin_priv']) if res else None
    def get_all_persons(self):
        res = self._send_req('onp_get_people', {'from': 0, 'count': self.MAX_ELEMENTS})
        return res and res.get('data', None)
    def check_session(self):
        return self._send_req('onp_check_session', {})
    def logout(self):
        return self._send_req('onp_logout', {})
    def add_school_type(self, school_type):
        return self._send_req('onp_add_school_type', school_type)
    def get_school_types(self):
        r = self._send_req('onp_get_school_types', {'from': 0, 'count': self.MAX_ELEMENTS})
        return r and r.get('data', None)
    def add_city_type(self, city_type):
        return self._send_req('onp_add_city_type', city_type)
    def get_city_types(self):
        r = self._send_req('onp_get_city_types', {'from': 0, 'count': self.MAX_ELEMENTS})
        return r and r.get('data', None)
    def get_cities(self):
        r = self._send_req('onp_get_cities', {'from': 0, 'count': self.MAX_ELEMENTS})
        return r and r.get('data', None)
    def add_criteria_title(self, title):
        return self._send_req('onp_add_criteria_title', title)
    def get_criteria_titles(self):
        r = self._send_req('onp_get_criteria_titles', {'from': 0, 'count': self.MAX_ELEMENTS})
        return r and r.get('data', None)
    def get_competitions(self):
        r = self._send_req('onp_get_competitions', {'from': 0, 'count': self.MAX_ELEMENTS})
        return r and r.get('data', None)
    def get_schools(self):
        r = self._send_req('onp_get_schools', {'from': 0, 'count': self.MAX_ELEMENTS})
        return r and r.get('data', None)
