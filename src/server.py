"""
Web Server
"""
from sanic import Sanic
from sanic.response import json
from sanic.response import text
from pymysql.constants import CLIENT
import pymysql
import time
import mid

app = Sanic("hello")

err_log_list = [
    # tautology error log
    ["/root/app/expand/sql_log/error_tautology.txt","/root/app/sql_log/error_tautology.txt","/root/app/sql_log/syntax_error/tautology_1064.txt"], 
    # illegal error log
    ["/root/app/expand/sql_log/error_illegal.txt","/root/app/sql_log/error_illegal.txt","/root/app/sql_log/syntax_error/illegal_1064.txt"], 
    # union error log
    ["/root/app/expand/sql_log/error_union.txt","/root/app/sql_log/error_union.txt","/root/app/sql_log/syntax_error/union_1064.txt"], 
    # bool_blind error log
    ["/root/app/expand/sql_log/error_bool_blind.txt","/root/app/sql_log/error_bool_blind.txt","/root/app/sql_log/syntax_error/bool_blind_1064.txt"], 
    # time_blind error log
    ["/root/app/expand/sql_log/error_time_blind.txt","/root/app/sql_log/error_time_blind.txt","/root/app/sql_log/syntax_error/time_blind_1064.txt"], 
    # normal error log
    ["/root/app/expand/sql_log/error_normal.txt","/root/app/sql_log/error_normal.txt","/root/app/sql_log/syntax_error/normal_1064.txt"], 
]

# Route "/": GET method
@app.route("/")
async def handler_root(request):
    db = pymysql.connect(host="localhost",user="root",password="",database="mysql")
    cursor = db.cursor()
    cursor.execute("select @@version")
    data = cursor.fetchone()
    db.close()
    return json({"version":data})


# Route "/test": POST method, accepted parameters: count, user, formal, type
@app.post("/test")
async def handler_post(request):
    line = request.form.get("count")                # line number
    payload = request.form.get("user")              # malicious payload
    is_formal = int( request.form.get("formal") )   # 1 - formal request，0 - other request
    sql_type = int( request.form.get("type") )      # sql_type: 0 - tautology, 1 - illegal, 2 - union, 3 - bool_blind, 4 - time_blind, 5 - normal
    sql = ''
    results = []
    # config for connecting DB
    conf = {
        "host": "localhost",
        "password": "",
        "user": "root",
        "client_flag": CLIENT.MULTI_STATEMENTS,     # Multiple queries separated by semicolons can be executed at one time
        "database": "info"
    }
    
    db = pymysql.connect(**conf)
    cursor = db.cursor()
    
    try:
        sql = mid.logs(sql_type, payload, is_formal)
        cursor.execute(sql)
        results.append(cursor.fetchall())
        # obtain all query results when executing multiple query statements
        while (cursor.nextset()):
            results.append(cursor.fetchall())
        db.commit()
    
    except pymysql.Error as e:
        db.rollback()
        # write sql errors into error.txt
        timestamp = time.strftime("%m-%d %H:%M:%S", time.localtime())
        with open(err_log_list[sql_type][is_formal], "a") as f:
            f.write("[" + timestamp + "] [" + line + "] - [ERROR] : " + str(e) + '\n')
            f.write("[" + timestamp + "] [" + line + "] - [SQLi]: " + payload + '\n')
            f.write("[" + timestamp + "] [" + line + "] - [SQL]: " + sql + '\n')
        # write syntax errors
        if (e.args[0] == 1064):
            with open(err_log_list[sql_type][2], "a") as f:
                f.write("[" + timestamp + "] [" + line + "] - [ERROR] : " + str(e) + '\n')
                f.write("[" + timestamp + "] [" + line + "] - [SQLi]: " + payload + '\n')
                f.write("[" + timestamp + "] [" + line + "] - [SQL]: " + sql + '\n')
    db.close()
    
    return text(str(results))


# Route "/normal": POST method, accepted parameters: params, count, formal, type
@app.post("/normal")
async def handler_normal_post(request):
    payload = request.form.get("params")            # any type of user input: number or str
    line = request.form.get("count")                # line number
    is_formal = int( request.form.get("formal") )   # 1 - formal request，0 - other request
    sql_type = int( request.form.get("type") )      # sql_type: 0 - tautology, 1 - illegal, 2 - union, 3 - bool_blind, 4 - time_blind, 5 - normal
    sql = ''
    results = []
    # config for connecting DB
    conf = {
        "host": "localhost",                   
        "port": 3307,                           # middleware listening port
        "password": "",
        "user": "root",
        "client_flag": CLIENT.MULTI_STATEMENTS, # Multiple queries separated by semicolons can be executed at one time
        "database": "info"
    }
    db = pymysql.connect(**conf)
    cursor = db.cursor()
    
    try:
        sql = mid.get_normal_sql(payload, sql_type)
        cursor.execute(sql)
        results.append(cursor.fetchall())
        # obtain all query results when executing multiple query statements
        while (cursor.nextset()):
            results.append(cursor.fetchall())
        db.commit()

    except pymysql.Error as e:
        db.rollback()
        # write sql errors into error.txt
        timestamp = time.strftime("%m-%d %H:%M:%S", time.localtime())
        with open(err_log_list[sql_type][is_formal], "a") as f:
            f.write("[" + timestamp + "] [" + line + "] - [ERROR] : " + str(e) + '\n')
            f.write("[" + timestamp + "] [" + line + "] - [SQLi]: " + payload + '\n')
            f.write("[" + timestamp + "] [" + line + "] - [SQL]: " + sql + '\n')
        # write syntax errors
        if (e.args[0] == 1064):
            with open(err_log_list[sql_type][2], "a") as f:
                f.write("[" + timestamp + "] [" + line + "] - [ERROR] : " + str(e) + '\n')
                f.write("[" + timestamp + "] [" + line + "] - [SQLi]: " + payload + '\n')
                f.write("[" + timestamp + "] [" + line + "] - [SQL]: " + sql + '\n')
    db.close()
    
    return text(str(results))


if __name__=="__main__":
    app.run(host="0.0.0.0",port=8888,debug=True)
