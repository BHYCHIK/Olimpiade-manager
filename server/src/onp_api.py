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

def _session_checker(request, sess):
    if not sess or sess["ip_addr"] != request["ip_addr"].host:
        return False
    return True

def _fetch_one_dict(cursor):
    data = cursor.fetchone()
    if data == None:
        return None
    desc = cursor.description

    res = {}

    for (name, value) in zip(desc, data) :
        res[name[0]] = value

    return res

def _fetch_all_dict(cursor):
    result = []
    while True:
        row = _fetch_one_dict(cursor)
        if not row:
            break
        result.append(row)
    return result

def _exec_sql_get_func(request, sql):
    conf = config.Config()
    mysql_exception = None
    try:
        conn = MySQLdb.connect(host=conf.db_host, user = conf.db_user, passwd = conf.db_pass, db = conf.db_name)
    except Exception, e:
        mysql_exception = e
        logger.Logger().error("SQL ERROR: " + str(mysql_exception))
        return sql_error(request, str(mysql_exception))
    cur = conn.cursor()

    error_happend = False
    inserted_id = 0
    try:
        cur.execute(sql, request)
        data = _fetch_all_dict(cur)
    except MySQLdb.Error, e:
         error_happend = True
         mysql_exception = e
    finally:
        cur.close()
        conn.close()
    if error_happend:
        logger.Logger().error("SQL ERROR: " + str(mysql_exception))
        return sql_error(request, str(mysql_exception))

    result = {}
    result["error_code"] = 0
    result["id"] = int(request["id"])
    result["data"] = data

    return result

def onp_ping(request):
    result = {}
    result["error_code"] = 0;
    result["id"] = int(request["id"])
    return result

def onp_logout(request):
    if not _check_args(request, "session_id"):
        return not_enough_args(request)
    session.delete_session(request["session_id"])
    result = {}
    result["error_code"] = 0
    result["id"] = int(request["id"])
    return result

def onp_check_session(request):
    if not _check_args(request, "session_id"):
        return not_enough_args(request)
    sess = session.get_session(request["session_id"])
    if not _session_checker(request, sess):
        return not_enough_rights(request)
    return {"error_code": 0, "id": request["id"]}

def onp_get_people(request):
    if not _check_args(request, "from", "count", "session_id"):
        return not_enougth_args(request)
#    sess = session.get_session(request["session_id"])
#    if not _session_checker(request, sess):
#        return not_enough_rights(request)

    sql = "SELECT id, first_name, second_name, surname, gender, email, date_of_birth, description, address, phone from person order by surname, first_name, second_name, id limit %(from)s, %(count)s"
    result = _exec_sql_get_func(request, sql)
    if result["error_code"] != 0:
        return result
    for person in result["data"]:
        try:
            person["date_of_birth"] = person["date_of_birth"].strftime("%Y%m%d")
        except Exception:
            person["date_of_birth"] = "00000000"
    return result

def onp_get_city_types(request):
    if not _check_args(request, "from", "count", "session_id"):
        return not_enougth_args(request)
    sess = session.get_session(request["session_id"])
    if not _session_checker(request, sess):
        return not_enough_rights(request)
    sql = "SELECT id, short_title, full_title from city_type order by id limit %(from)s, %(count)s"
    result = _exec_sql_get_func(request, sql)
    return result

def onp_get_cities(request):
    if not _check_args(request, "from", "count", "session_id"):
        return not_enougth_args(request)
    sess = session.get_session(request["session_id"])
    if not _session_checker(request, sess):
        return not_enough_rights(request)

    sql = "SELECT id, name from city order by name limit %(from)s, %(count)s"

    result = _exec_sql_get_func(request, sql)
    return result

def onp_get_criteria_titles(request):
    if not _check_args(request, "from", "count", "session_id"):
        return not_enougth_args(request)
    sess = session.get_session(request["session_id"])
    if not _session_checker(request, sess):
        return not_enough_rights(request)

    sql = "SELECT id, short_name, full_name FROM criteria_title ORDER BY id LIMIT %(from)s, %(count)s"

    result = _exec_sql_get_func(request, sql)
    return result

def onp_get_school_types(request):
    if not _check_args(request, "from", "count", "session_id"):
        return not_enougth_args(request)
    sess = session.get_session(request["session_id"])
    if not _session_checker(request, sess):
        return not_enough_rights(request)

    sql = "SELECT id, short_title, full_title, full_name FROM school_type ORDER BY id LIMIT %(from)s, %(count)s"

    result = _exec_sql_get_func(request, sql)
    return result

def _add_entry(request, sql, result_field, only_auth = True, admin_only_true = False):
    sess = session.get_session(request["session_id"])
    #if only_auth:
        #if not _session_checker(request, sess):
        #        return not_enough_rights(request)
        #if admin_only_true and (int(sess["admin_priv"]) == 0):
        #    return not_enough_rights(request)
    conf = config.Config()
    mysql_error = None
    try:
        conn = MySQLdb.connect(host=conf.db_host, user = conf.db_user, passwd = conf.db_pass, db = conf.db_name)
    except MySQLdb.Error, e:
        return sql_error(request, str(mysql_error))
    cur = conn.cursor()

    error_happend = False
    inserted_id = 0
    try:
        cur.execute(sql, request)
        inserted_id = conn.insert_id()
        conn.commit()
    except MySQLdb.Error, e:
         error_happend = True
         mysql_error = e
    finally:
        cur.close()
        conn.close()
    if error_happend:
        return sql_error(request, str(mysql_error))

    result = {}
    result["error_code"] = 0
    result["id"] = int(request["id"])
    result[result_field] = inserted_id
    return result

def onp_add_criteria_title(request):
    if not _check_args(request, "short_name", "full_name", "session_id"):
        return not_enougth_args(request)
    sql = "INSERT INTO criteria_title(short_name, full_name) VALUES(%(short_name)s, %(full_name)s)"
    return _add_entry(request, sql, "criteria_title_id", True, True)
    return result

def onp_add_city(request):
    if not _check_args(request, "name", "city_type_id", "session_id"):
        return not_enougth_args(request)
    sql = "INSERT INTO city(name, city_type_id) VALUES(%(name)s, %(city_type_id)s)"
    return _add_entry(request, sql, "city_id", True, True)

def onp_add_city_type(request):
    if not _check_args(request, "short_title", "full_title", "session_id"):
        return not_enougth_args(request)
    sql = "INSERT INTO city_type(short_title, full_title) VALUES(%(short_title)s, %(full_title)s)"
    return _add_entry(request, sql, "city_type_id", True, True)

def onp_add_school_type(request):
    if not _check_args(request, "short_title", "full_title", "session_id"):
        return not_enougth_args(request)
    sql = "INSERT INTO school_type(short_title, full_title) VALUES(%(short_title)s, %(full_title)s)"
    return _add_entry(request, sql, "school_type_id", True, True)

def onp_register_person(request):
    if not _check_args(request, "first_name", "second_name", "surname", "gender", "email", "date_of_birth", "description", "address", "phone", "session_id"):
        return not_enougth_args(request)
    sql = "INSERT INTO person(first_name, second_name, surname, gender, email, date_of_birth, description, address, phone) VALUES(%(first_name)s, %(second_name)s, %(surname)s, %(gender)s, %(email)s, %(date_of_birth)s, %(description)s, %(address)s, %(phone)s)"
    return _add_entry(request, sql, "person_id", True, True)

def onp_register_account(request):
    if not _check_args(request, "login", "password", "person_id", "session_id", "admin_priv"):
        return not_enougth_args(request)
    sql = "INSERT INTO account(login, password_hash, person_id, admin_priv) VALUES(%(login)s, md5(%(password)s), %(person_id)s, %(admin_priv)s)"
    return _add_entry(request, sql, "account_id", True, True)

def onp_request_session(request):
    if not _check_args(request, "login", "password"):
        return not_enougth_args(request)
    try:
        sess = session.make_session(request)
    except MySQLdb.Error, e:
        return sql_error(request, str(e))
    except session.UnknownUserException:
        return incorrect_account(request)
    except session.MemcacheException:
        return internal_error(request)
    result = {}
    result["error_code"] = 0
    result["id"] = int(request["id"])
    result["session_id"] = sess["session_id"]
    result["admin_priv"] = sess["admin_priv"]
    result["person_id"] = sess["person_id"]
    return result

api_functions = {
    "onp_ping": onp_ping,
    "onp_register_person": onp_register_person,
    "onp_register_account": onp_register_account,
    "onp_logout": onp_logout,
    "onp_check_session": onp_check_session,
    "onp_get_people": onp_get_people,
    "onp_add_criteria_title": onp_add_criteria_title,
    "onp_add_school_type": onp_add_school_type,
    "onp_add_city_type": onp_add_city_type,
    "onp_add_city": onp_add_city,
    "onp_get_cities": onp_get_cities,
    "onp_get_city_types": onp_get_city_types,
    "onp_get_criteria_titles": onp_get_criteria_titles,
    "onp_get_school_types": onp_get_school_types,
    "onp_request_session": onp_request_session
}
