# -*- coding:utf-8 -*-
from bottle import request, response
import db_create_tables as db
import time, datetime
import config
import hashlib
import twitter_client as tc

dbname = './example.db'


def authorize(request):

    """
     　request に対して、(username, password)をチェックし、
     　認証できたら True, そうでなければ False を返す。
    """
    
    username = request.forms.get("username")
    password = request.forms.get("password")

    print("USERNAME: {}".format(username))
    print("PASSWORD: {}".format(password))

    # DBアクセス
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    result = db.search_user_password(cursor, username, password)
    conn.close()
    
    return result

def authorize_sessionid(request):

    # RequestのSession IDの取得 ##
    sessionid = request.get_cookie("session")
    print("Request Session ID: " + str(sessionid))

    # DBアクセスし、Session IDをチェック
    if sessionid != '' and sessionid != None:
        # DBアクセス
        conn = db.connect_db(dbname)
        cursor = db.get_cursor(conn)
        result = db.check_sessionid(cursor, sessionid)
        # 有効期間の更新
        if result == True:
            db.extend_validate_period(cursor, sessionid)
            db.commit(conn)
        conn.close()
        return result
    else:
        return False
    
def generate_sessionid():
    
    # session IDの生成 (hash関数を使う)
    sessionid_src = str(datetime.datetime.now()) + config.RANDOM_SEED
    print("Session ID src: " + sessionid_src)
    sessionid = hashlib.sha256(sessionid_src.encode()).hexdigest()
    print("New Session ID: " + sessionid)
    # session IDのDBへの登録
    # DBアクセス
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    db.register_sessionid(cursor, sessionid)
    db.commit(conn)
    conn.close()

    return sessionid

def login(request):

    # login認証
    login_status = authorize(request)
    print("Login authorization:" +str(login_status))

    # login認証に成功
    if ( login_status ):
        # Session ID生成
        sessionid = generate_sessionid()
        # Session IDセット
        response.set_cookie("session", sessionid)

    # login認証に失敗
    else:
        login_status = False

    return login_status

