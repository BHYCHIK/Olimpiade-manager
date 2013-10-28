# This file contains functions that returns jsons replies on incorrect requests
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013

def _make_err_dict(code, text, id = None):
    result = dict()
    result["error_code"] = code
    result["error_text"] = text
    if (id is not None):
        result["id"] = id
    return result

def request_not_valid_json():
    return _make_err_dict(1, "Your request is not valid json")

def unknown_api_function(request):
    return _make_err_dict(2, "Unknown api function or no cmd field in request", int(request["id"]))

def no_id_parametr():
    return _make_err_dict(3, "No id parametr");

def not_enougth_args(request):
    return _make_err_dict(4, "No enough parametr", int(request["id"]));

def sql_error(request, text = ""):
    return _make_err_dict(5, "Sql error: " + text, int(request["id"]))

def incorrect_account(request):
    return _make_err_dict(6, "Incorrect login or password", int(request["id"]))

def not_enough_rights(request):
    return _make_err_dict(7, "You are not authorized or not enough rights", int(request["id"]))

def internal_error(request):
    return _make_err_dict(500, "Internal server error", int(request["id"]))

def unknown_error():
    return _make_err_dict(999, "Unknown error")
