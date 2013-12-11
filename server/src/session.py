# *-* coding: utf-8 *-*

import memcache
import string
import random
import config
import MySQLdb
import json
import logger

class UnknownUserException(BaseException): pass
class MemcacheException(BaseException): pass

def _fetch_one_dict(cursor):
    data = cursor.fetchone()
    if data == None:
        return None
    desc = cursor.description

    res = {}

    for (name, value) in zip(desc, data) :
        res[name[0]] = value.decode('utf-8') if isinstance(value, str) else value

    return res

def _fetch_all_dict(cursor):
    result = []
    while True:
        row = _fetch_one_dict(cursor)
        if not row:
            break
        result.append(row)
    return result

def _get_roles(person_id):
    sql = "SELECT id, competition_id, role from role where person_id=%(person_id)s"
    sql_args = {}
    sql_args["person_id"] = person_id

    conf = config.Config()
    mysql_exception = None
    try:
        conn = MySQLdb.connect(host=conf.db_host, charset="utf8", use_unicode=True, user=conf.db_user, passwd=conf.db_pass, db=conf.db_name)
    except Exception, e:
        mysql_exception = e
        logger.Logger().error(u"Ошибка СУБД: " + str(mysql_exception))
        raise mysql_exception
    cur = conn.cursor()

    error_happend = False
    inserted_id = 0
    try:
        cur.execute(sql, sql_args)
        data = _fetch_all_dict(cur)
    except MySQLdb.Error, e:
         error_happend = True
         mysql_exception = e
    finally:
        cur.close()
        conn.close()
    if error_happend:
        logger.Logger().error(u"Ошибка СУБД: " + str(mysql_exception))
        raise mysql_exception
    return data

def _gen_session_id():
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(64)]
    str = "".join(lst)
    return str


# Can raise MySQLdb exceptions
def _check_pass(request):
    mysql_exception = None

    conf = config.Config()
    conn = MySQLdb.connect(host=conf.db_host, charset="utf8", use_unicode=True, user = conf.db_user, passwd = conf.db_pass, db = conf.db_name)
    cur = conn.cursor()

    sql = "SELECT id, person_id, admin_priv from account where login=%(login)s and password_hash=md5(%(password)s)"

    error_happend = False
    row = None
    try:
        cur.execute(sql, request)
        row = cur.fetchone()
    except MySQLdb.Error, e:
        error_happend = True
        mysql_exception = e
        logger.Logger().error(u"Ошибка СУБД: " + str(mysql_exception))
    finally:
        cur.close()
        conn.close()

    if error_happend:
        raise mysql_exception

    if row is None:
        logger.Logger().warn(u"Неверный логин или пароль для пользователя %s" % request["login"])
        raise UnknownUserException()

    return row


def make_session(request):
    conf = config.Config()
    account_info = _check_pass(request)
    session = dict()
    session["ip_addr"] = request["ip_addr"].host
    session["person_id"] = account_info[1]
    session["admin_priv"] = account_info[2]
    session["roles"] = _get_roles(account_info[1])

    mc = memcache.Client([conf.memcached_addr], debug=0)
    sess_id = _gen_session_id()
    session["session_id"] = sess_id
    mc_result = mc.set(key = sess_id, val = json.dumps(session), time = conf.session_timeout)
    mc.disconnect_all()

    if mc_result == 0:
        logger.Logger().error(u"Ошибка системы кэширования (номер сессии = %s, логин= %s)" % (sess_id, request["login"]) )
        raise MemcacheException()
    return session

def get_session(sess_id):
    conf = config.Config();
    mc = memcache.Client([conf.memcached_addr], debug=0)

    try:
        res = mc.get(sess_id.encode('utf-8'))
    except memcache.Client.MemcachedKeyError as error:
        logger.Logger().error(u"Ошибка системы кэширования: %s" % error)
        return None
    if not res:
        return None
    r = json.loads(res)
    r["roles"] = _get_roles(r["person_id"])
    return r

def delete_session(sess_id):
    conf = config.Config();
    mc = memcache.Client([conf.memcached_addr], debug=0)
    try:
        mc.delete(sess_id.encode('utf-8'))
    except memcache.Client.MemcachedKeyError as e:
        logger.Logger().warn(u"Ошибка системы кэширования: " + str(e))
