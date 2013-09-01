# This file contains functions that returns jsons replies on incorrect requests
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013

def request_not_valid_json():
    return '{"error_code": 1, "error_text": "Your request is not valid json"}'

def unknown_api_function(request):
    return '{"error_code": 2, "id": %d, "error_text": "Unknown api function or no cmd field in request"}' % int(request["id"])

def no_id_parametr():
    return '{"error_code": 3, "error_text": "No id parametr"}'

def not_enougth_args(request):
    return '{"error_code": 4, "error_text": "No enough parametr", "id": %d}' % int(request["id"])

def sql_error(request):
    return '{"error_code": 5, "error_text": "Sql error", "id": %d}' % int(request["id"])

def unknown_error():
    return '{"error_code": 999, "error_text": "Unknown error"}'
