import datetime
import time
import settings
import socket
import json
from django.shortcuts import render_to_response
from django.template import RequestContext

def xor_crypt_string(data, key, encode=False, decode=False):
    from itertools import izip, cycle
    import base64
    if decode:
        data = base64.decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    if encode:
        return base64.encodestring(xored).strip()
    return xored

def get_backend_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', settings.BROADCAST_PORT))
    data, addr = s.recvfrom(8192)
    decrypted_data = xor_crypt_string(data, settings.BROADCAST_PASS, False, True)
    print('Got from broadcasting %s, after decryption - %s' % (data, decrypted_data))
    s.close()
    return (addr[0], settings.BACKEND_PORT)

class ApiUser(object):
    def __init__(self, request):
        if 'id' in request.session:
            session_id = request.session['id']
            self._session_id = session_id
            self._api = Api(session_id, get_backend_ip())
            self._is_authenticated = self.get_api().check_session()
            self._is_admin = True if request.session['admin_priv'] else False
        else:
            self._is_authenticated = False
            self._api = None
        print('[%s]: is authenticated = %s' % (request.path, str(self._is_authenticated)))
    def get_api(self):
        return self._api
    def login(self, request, login, password):
        session_id, admin_priv = self.get_api().account_login({'login': login, 'password': password})
        if session_id:
            request.session['id'] = session_id
            request.session['admin_priv'] = admin_priv
        return session_id

    def logout(self):
        return self.get_api().logout()
    def is_authenticated(self):
        return self._is_authenticated
    def is_admin(self):
        return self.is_authenticated() and self._is_admin

    @staticmethod
    def login_required(func):
        def wrapper(request, *args, **kwargs):
            if request.api_user.is_authenticated():
                return func(request, request.api_user.get_api(), *args, **kwargs)
            return render_to_response('common/no_access.html',
                                      context_instance=RequestContext(request))
        return wrapper

    @staticmethod
    def admin_required(func):
        def wrapper(request, *args, **kwargs):
            if request.api_user.is_admin():
                return func(request, request.api_user.get_api(), *args, **kwargs)
            return render_to_response('common/no_access.html',
                                      context_instance=RequestContext(request))
        return wrapper


class Api(object):
    ERR_CODE_OK = 0
    MAX_ELEMENTS = 1000

    def __init__(self, session_id=None, backend_ip=None):
        self._session_id = session_id
        self.backend_ip = backend_ip or settings.BACKEND_HOST

    def _send_req(self, cmd, data):
        json_data = dict(data)
        json_data.update({'id': 1, 'cmd': cmd, 'ip_addr': '127.0.0.1', 'session_id': self._session_id})
        print('[%s]: frontend is trying to send %s to backend' % (cmd, json.dumps(json_data)))
        try:
            sock = socket.create_connection(self.backend_ip, settings.BACKEND_TIMEOUT)
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
    def get_schools(self):
        r = self._send_req('onp_get_schools', {'from': 0, 'count': self.MAX_ELEMENTS})
        return r and r.get('data', None)
    def add_school(self, school):
        return self._send_req('onp_add_school', school)
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
    def start_competition(self, year):
        return self._send_req('onp_start_competition', year)
    def get_competitions(self):
        r = self._send_req('onp_get_competitions', {'from': 0, 'count': self.MAX_ELEMENTS})
        return r and r.get('data', None)
    def get_competition_participants(self, competition_id):
        r = self._send_req('onp_get_competition_pariticipants', {'from': 0, 'count': self.MAX_ELEMENTS, 'competition_id': competition_id})
        return r and r.get('data', None)
    def get_city(self, city_id):
        r = self._send_req('onp_get_city', {'city_id': city_id})
        return r and r.get('data', None)
    def add_city(self, city):
        return self._send_req('onp_add_city', city)
