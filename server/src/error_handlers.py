# This file contains functions that returns jsons replies on incorrect requests
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013

def request_not_valid_json():
    return '{"error_code": 1, "error_text": "Your request is not valid json"}'

def unknown_api_function(request):
    return '{"error_code": 2, id: %d, "error_text": "Unknown api function or no cmd field in request"}' % request["id"]

def no_id_paramter():
    return '{"error_code": 3, "error_text": "No id parametr"}'
