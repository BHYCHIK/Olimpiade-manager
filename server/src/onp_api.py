# This file contains api functions
# Copyright Ivan Remen (i.remen@corp.mail.ru) BMSTU 2013
import MySQLdb
from error_handlers import *
import config
import logger

def _check_args(request, *needed_args):
    for arg in needed_args:
        if request.get(arg, None) is None:
            logger.Logger().debug("No argument %s" % arg)
            return False
    return True

def onp_ping(request):
    return '{"error_code": 0, "id": %d}' % request["id"]

def onp_register_person(request):
    if not _check_args(request, "first_name", "second_name", "surname", "gender", "email", "date_of_birth", "description", "address", "phone"):
        return not_enougth_args(request)
    conf = config.Config()
    conn = MySQLdb.connect(host=conf.db_host, user = conf.db_user, passwd = conf.db_pass, db = conf.db_name)
    cur = conn.cursor()

    sql = "INSERT INTO person(first_name, second_name, surname, gender, email, date_of_birth, desciption, address, phone) VALUES(%(first_name)s, %(second_name)s, %(surname)s, %(gender)s, %(email)s, %(date_of_birth)s, %(description)s, %(address)s, %(phone)s)"

    cur.execute(sql, request)
    inserted_id = conn.insert_id()
    conn.commit()

    return '{"error_code": 0, "id": %d, "person_id": %d}' % (request["id"], inserted_id)

    cur.close()
    conn.close()

def onp_register_account(request):
    if not _check_args(request, "login", "password", "person_id"):
        return not_enougth_args(request)
    conf = config.Config()
    conn = MySQLdb.connect(host=conf.db_host, user = conf.db_user, passwd = conf.db_pass, db = conf.db_name)
    cur = conn.cursor()

    sql = "INSERT INTO account VALUES(%(login)s, md5(%(password)s), %(person_id)d)"

    cur.execute(sql, request)
    conn.commit()
    inserted_id = conn.insert_id()

    return '{"error_code": 0, "id": %d, "account_id": %d}' % (request["id"], inserted_id)

    cur.close()
    conn.close()

api_functions = {
    "onp_ping": onp_ping,
    "onp_register_person": onp_register_person,
    "onp_register_account": onp_register_account
}
