# This file contains api functions
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013
import MySQLdb
from error_handlers import *
import config
import logger
import session

def _check_args(request, *needed_args):
    for arg in needed_args:
        if request.get(arg, None) is None:
            logger.Logger().debug("No argument %s" % arg)
            return False
    return True

def onp_ping(request):
    return '{"error_code": 0, "id": %d}' % int(request["id"])

def onp_logout(request):
    if not _check_args(request, "session_id"):
        return not_enough_args(request)
    session.delete_session(request["session_id"])
    return '{"error_code": 0, "id": %d}' % int(request["id"])

def onp_register_person(request):
    if not _check_args(request, "first_name", "second_name", "surname", "gender", "email", "date_of_birth", "description", "address", "phone", "session_id"):
        return not_enougth_args(request)
    if not sess or int(sess["admin_priv"]) == 0:
        return not_enough_rights(request)
    conf = config.Config()
    try:
        conn = MySQLdb.connect(host=conf.db_host, user = conf.db_user, passwd = conf.db_pass, db = conf.db_name)
    except Exception:
        return sql_error(request)
    cur = conn.cursor()

    sql = "INSERT INTO person(first_name, second_name, surname, gender, email, date_of_birth, description, address, phone) VALUES(%(first_name)s, %(second_name)s, %(surname)s, %(gender)s, %(email)s, %(date_of_birth)s, %(description)s, %(address)s, %(phone)s)"

    error_happend = False
    inserted_id = 0
    try:
        cur.execute(sql, request)
        inserted_id = conn.insert_id()
        conn.commit()
    except Exception:
         error_happend = True
    finally:
        cur.close()
        conn.close()
    if error_happend:
        return sql_error(request)

    return '{"error_code": 0, "id": %d, "person_id": %d}' % (int(request["id"]), inserted_id)

def onp_register_account(request):
    if not _check_args(request, "login", "password", "person_id", "session_id"):
        return not_enougth_args(request)
    sess = session.get_session(request["session_id"])
    if not sess or int(sess["admin_priv"]) == 0:
        return not_enough_rights(request)
    conf = config.Config()
    try:
        conn = MySQLdb.connect(host=conf.db_host, user = conf.db_user, passwd = conf.db_pass, db = conf.db_name)
    except Exception:
        return sql_error(request)

    cur = conn.cursor()

    sql = "INSERT INTO account(login, password_hash, person_id) VALUES(%(login)s, md5(%(password)s), %(person_id)s)"

    error_happend = False
    inserted_id = 0
    try:
        cur.execute(sql, request)
        conn.commit()
        inserted_id = conn.insert_id()

    except Exception:
        error_happend = True

    finally:
        cur.close()
        conn.close()
    if error_happend:
        return sql_error(request)

    return '{"error_code": 0, "id": %d, "account_id": %d}' % (int(request["id"]), inserted_id)

def onp_request_session(request):
    if not _check_args(request, "login", "password"):
        return not_enougth_args(request)
    try:
        sess = session.make_session(request)
        return '{"error_code": 0, "id": %d, "session_id": "%s", "admin_priv": "%s", "person_id": %d}' % (int(request["id"]), sess["session_id"], sess["admin_priv"], sess["person_id"])
    except MySQLdb.Error:
        return sql_error(request)
    except session.UnknownUserException:
        return incorrect_account(request)
    except session.MemcacheException:
        return internal_error(request)

api_functions = {
    "onp_ping": onp_ping,
    "onp_register_person": onp_register_person,
    "onp_register_account": onp_register_account,
    "onp_logout": onp_logout,
    "onp_request_session": onp_request_session
}
