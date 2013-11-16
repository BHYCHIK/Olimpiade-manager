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
    return _make_err_dict(1, u"Ваш запрос имеет неверный формат")

def unknown_api_function(request):
    return _make_err_dict(2, u"Не найдена функция, представленная в Вашем запросе", int(request["id"]))

def no_id_parametr():
    return _make_err_dict(3, u"Нет параметра id");

def not_enougth_args(request):
    return _make_err_dict(4, u"Не хватает параметров", int(request["id"]));

def sql_error(request, text = ""):
    return _make_err_dict(5, u"Ошибка СУБД: " + text, int(request["id"]))

def incorrect_account(request):
    return _make_err_dict(6, u"Неверный логин или пароль", int(request["id"]))

def not_enough_rights(request):
    return _make_err_dict(7, u"Вы неавторизованны или Вам не хватает прав", int(request["id"]))

def internal_error(request):
    return _make_err_dict(500, u"Внутреняя ошибка сервера", int(request["id"]))

def unknown_error():
    return _make_err_dict(999, u"Неизвестная ошибка")
