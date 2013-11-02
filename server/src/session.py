import memcache
import string
import random
import config
import MySQLdb
import json
import logger

class UnknownUserException(BaseException): pass
class MemcacheException(BaseException): pass

def _gen_session_id():
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(64)]
    str = "".join(lst)
    return str


# Can raise MySQLdb exceptions
def _check_pass(request):
    mysql_exception = None

    conf = config.Config()
    conn = MySQLdb.connect(host=conf.db_host, user = conf.db_user, passwd = conf.db_pass, db = conf.db_name)
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
        logger.Logger().error("SQL ERROR: " + str(mysql_exception))
    finally:
        cur.close()
        conn.close()

    if error_happend:
        raise mysql_exception

    if row is None:
        logger.Logger().warn("Incorrect login/password for %s" % request["login"])
        raise UnknownUserException()

    return row


def make_session(request):
    conf = config.Config()
    account_info = _check_pass(request)
    session = dict()
    session["ip_addr"] = request["ip_addr"].host
    session["person_id"] = account_info[1]
    session["admin_priv"] = account_info[2]

    mc = memcache.Client([conf.memcached_addr], debug=0)
    sess_id = _gen_session_id()
    session["session_id"] = sess_id
    mc_result = mc.set(key = sess_id, val = json.dumps(session), time = conf.session_timeout)
    mc.disconnect_all()

    if mc_result == 0:
        logger.Logger().error("Something bad with memcached (sess_id = %s, login= %s)" % (sess_id, request["login"]) )
        raise MemcacheException()
    return session

def get_session(sess_id):
    conf = config.Config();
    mc = memcache.Client([conf.memcached_addr], debug=0)

    try:
        res = mc.get(sess_id.encode('utf-8'))
    except memcache.Client.MemcachedKeyError as error:
        logger.Logger().error("Memcached error: %s" % error)
        return None
    if not res:
        return None
    return json.loads(res)

def delete_session(sess_id):
    conf = config.Config();
    mc = memcache.Client([conf.memcached_addr], debug=0)
    try:
        mc.delete(sess_id.encode('utf-8'))
    except memcache.Client.MemcachedKeyError as e:
        logger.Logger().warn("Memcached error: " + str(e))
