"""
Middleware for generating SQL statement and logs
"""
import random
import time
import re

path_list = ["/root/app/expand/sql_log/","/root/app/sql_log/"]
type_list = ["tautology", "illegal", "union", "bool_blind", "time_blind", "normal"]


def logs(sql_type, payload, is_formal):
    """
    Write spliced SQL statements into logs  
    """
    timestamp = time.strftime("%m-%d", time.localtime())
    file = path_list[is_formal] + type_list[sql_type] + '_' + timestamp + ".txt"
    sql = concat_sql(payload, sql_type)
    with open(file, 'a') as f:
        f.write(sql + '\n')
    return sql


def concat_sql(payload, sql_type):
    """
    Splice SQL statements  
    
    Regular expression matches the first few characters of the malicious payload, and the matching templates are:
    (1) num, num), num)), num)))
    (2) str', str'), str')), str')))
    (3) str", str"), str")), str")))
    (4) left parenthesis only, str + comma
    """
    lower_payload = payload.lower()
    sql = ""
    if type_list[sql_type] != 'normal':
        # ")))
        if (re.search(r'^[-%\._a-zA-Z0-9]*"\){3}',lower_payload)):
            sql = "select username, password from info.admin where id < (select user_id from info.users where username not in (select login_user from info.login where not exists (select * from info.admin where username=\"%s\")))" % (lower_payload)
        # "))
        elif ( re.search(r'^[-%\._a-zA-Z0-9]*"\){2}',lower_payload) ):
            sql = "select rights,login, username from info.all_users where user_id in (select user_id from info.users where username not in (select login_user as username from info.login where username != \"%s\"))"  % (lower_payload)
        # ")
        elif ( re.search(r'^[-%\._a-zA-Z0-9]*"\)',lower_payload) ):
            sql = "select * from info.users where user_id in (select user_id from info.all_users where username=\"%s\")" % (lower_payload)
        # "
        elif ( re.search(r'^[-%\._a-zA-Z0-9]*"',lower_payload) ):
            sql = "select user_id, password from info.users where username=\"%s\"" % (lower_payload)
        # ')))
        elif (re.search(r'^[-%\._a-zA-Z0-9]*\'\){3}',lower_payload)):
            sql = "select username, password from info.admin where id < (select user_id from info.users where username not in (select login_user from info.login where not exists (select * from info.admin where username='%s')))" % (lower_payload)
        # '))
        elif (re.search(r'^[-%\._a-zA-Z0-9]*\'\){2}',lower_payload)):
            sql = "select rights,login, username from info.all_users where user_id in (select user_id from info.users where username not in (select login_user as username from info.login where username != '%s'))"  % (lower_payload)
        # ')
        elif (re.search(r'^[-%\._a-zA-Z0-9]*\'\)',lower_payload)):
            sql = "select * from info.users where user_id in (select user_id from info.all_users where username='%s')" % (lower_payload)
        # '
        elif (re.search(r'^[-%\._a-zA-Z0-9]*\'',lower_payload)):
            sql = "select user_id, password from info.users where username='%s'" % (lower_payload)
        # )))
        elif (re.search(r'^[-%\._a-zA-Z0-9]*\){3}',lower_payload)):
            sql = "select username, password from info.admin where id < (select user_id from info.users where username not in (select login_user from info.login where not exists (select * from info.admin where id=%s)))" % (lower_payload)
        # ))
        elif (re.search(r'^[-%\._a-zA-Z0-9]*\){2}',lower_payload)):
            sql = "select rights,login, username from info.all_users where user_id in (select user_id from info.users where username not in (select login_user as username from info.login where id = %s))"  % (lower_payload)
        # )
        elif (re.search(r'^[-%\._a-zA-Z0-9]*\)',lower_payload)):
            sql = "select * from info.users where user_id in (select user_id from info.all_users where user_id=%s)" % (lower_payload)
        # left parenthesis or number, letter, decimal point, -, %
        elif ( re.search(r'^\(',lower_payload) or re.search(r'^[-%\.\w]+,',lower_payload) ):
            sql = "select username, %s from info.users" % (lower_payload)
        # num
        else:
            sql = "select username, password, status from info.admin where id=%s" % (lower_payload)
    else:
        # User inputs column name of [users] table
        if lower_payload in ['user_id', 'group_id', 'fullname', 'user_nickname', 'display_name', 'user_email', 'password', 'rights', 'login']:
            sql = "select username, %s from info.users" % (lower_payload)
        # Uer inputs interger
        elif re.search(r'^\d+$', lower_payload):
            sql_list = [
                "select username, password from info.admin where id < (select user_id from info.users where username not in (select login_user from info.login where not exists (select * from info.admin where id=%s)))" % (lower_payload),
                "select rights,login, username from info.all_users where user_id in (select user_id from info.users where username not in (select login_user as username from info.login where id = %s))"  % (lower_payload),
                "select * from info.users where user_id in (select user_id from info.all_users where user_id=%s)" % (lower_payload),
                "select username, password, status from info.admin where id=%s" % (lower_payload)
            ]
            sql = random.choice(sql_list)
        # User inputs other string
        elif re.search(r'^[-%\._\w]+$', lower_payload):
            sql_list = [
                "select username, password from info.admin where id < (select user_id from info.users where username not in (select login_user from info.login where not exists (select * from info.admin where username=\"%s\")))" % (lower_payload),
                "select rights,login, username from info.all_users where user_id in (select user_id from info.users where username not in (select login_user as username from info.login where username != \"%s\"))"  % (lower_payload),
                "select * from info.users where user_id in (select user_id from info.all_users where username=\"%s\")" % (lower_payload),
                "select username, password from info.admin where id < (select user_id from info.users where username not in (select login_user from info.login where not exists (select * from info.admin where username='%s')))" % (lower_payload),
                "select rights,login, username from info.all_users where user_id in (select user_id from info.users where username not in (select login_user as username from info.login where username != '%s'))"  % (lower_payload),
                "select * from info.users where user_id in (select user_id from info.all_users where username='%s')" % (lower_payload),
                "select user_id, password from info.users where username='%s'" % (lower_payload)
            ]
            sql = random.choice(sql_list)
    
    return sql


# get normal sql statement from parameters of user requests
def get_normal_sql(payload, sql_type):
    sql = concat_sql(payload, sql_type)
    
    return sql
