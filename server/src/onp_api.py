# This file contains api functions
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013

def onp_ping(request):
    return '{"error_code": 0, "id": %d}' % request["id"]

api_functions = {
    "onp_ping": onp_ping
}
