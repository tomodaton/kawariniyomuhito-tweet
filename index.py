# -*- coding:utf-8 -*-
from bottle import route, run, request, response, HTTPResponse
from bottle import template
import json
import sqlite3
import db_create_tables as db
import time, datetime
import config
import hashlib

dbname = './example.db'
# dbname = './schetweet.db'


# 文字列(YYYY-MM-DD)で表される開始日付 from_date, 終了日付 to_dateから期間の日付リストを生成
def generate_dates(from_date, to_date):
    if from_date is None:
        from_datetime = datetime.datetime.now()
        from_date = from_datetime.strftime('%Y-%m-%d')
    else:
        from_datetime = datetime.datetime.strptime(from_date, '%Y-%m-%d')


    if to_date is None:
        to_datetime = from_datetime + datetime.timedelta(days=6)
        to_date = to_datetime.strftime('%Y-%m-%d')
    else:
        to_datetime = datetime.datetime.strptime(to_date, '%Y-%m-%d')

    dates = []
    datetime_l = from_datetime
    while datetime_l <= to_datetime:
        dates.append(datetime_l.strftime('%Y-%m-%d'))
        datetime_l = datetime_l + datetime.timedelta(days=1)
    return dates

def authorize(username, password):

    # DBアクセス
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)

    # import pdb; pdb.set_trace()
    # if username != '' and username != None:
    result = db.search_user_password(cursor, username, password)
    conn.close()
    
    return result

def authorize_sessionid(sessionid):

    # import pdb; pdb.set_trace()
    if sessionid != '' and sessionid != None:
        # DBアクセス
        conn = db.connect_db(dbname)
        cursor = db.get_cursor(conn)
        result = db.check_sessionid(cursor, sessionid)
        conn.close()
        return result
    else:
        return False
    
def generate_sessionid():
    

    # session IDの生成 (hash関数を使う)
    sessionid_src = str(datetime.datetime.now()) + config.RANDOM_SEED
    print("session id source: " + sessionid_src)
    sessionid = hashlib.sha256(sessionid_src.encode()).hexdigest()
    print("session id: " + sessionid)
    # session IDのDBへの登録
    # DBアクセス
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    db.register_sessionid(cursor, sessionid)
    db.commit(conn)
    conn.close()

    return sessionid

    
@route('/', method=['GET', 'POST'])
def index():

    input_username = request.forms.get("username")
    input_password = request.forms.get("password")

    print("USERNAME: {}".format(input_username))
    print("PASSWORD: {}".format(input_password))

    login = authorize(input_username, input_password)
    print(login)
    if ( login ):
        login = True

        # Session ID生成
        sessionid = generate_sessionid()
        # Session IDセット
        response.set_cookie("session", sessionid)

    else:
        login = False

    return template('index.tpl', login=login)


@route('/top.html', method='GET')
def top():

    ## 認証 ##
    print("Request Session ID: " + str(request.get_cookie("session")))
    # Session IDチェック (これは "/"以外のすべてのアクセスで行う。)
    # DBアクセス
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    sessionid = request.get_cookie("session")

    sessionid_valid = authorize_sessionid(sessionid)

    if ( sessionid_valid == False ):
        header = {"Content-Type": "application/text"}
        res = HTTPResponse(status=302, headers=header)
        res.set_header('location', '/')
        return res
    ## 認証ここまで ##

    from_date = request.query.get('from_date')
    to_date = request.query.get('to_date')
    
    dates = generate_dates(from_date, to_date)


    groups = {}
    tweets = {}
    for date in dates:
        results = db.search_group_by_date(cursor, date)
        groups[date]= results
        for group in results:
            tweets[group['gid']] = db.search_tweets_by_gid(cursor, group['gid'])
    print('tweets: '+str(tweets))
    db.close_db(conn)
            
    return template('top3.tpl', dates=dates, groups=groups, tweets=tweets)


# API
# ツイートグループ 追加/更新/検索(by date, by gid)/削除
# ツイート 追加/更新/検索(by gid)/削除
@route('/api/1.0/add_tweet_group.json', method=["POST"])
def api_add_tweet_group():
    body = request.json

    sched_start_date = body['sched_start_date']
    interval = body['interval']
    
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    result = db.add_group(cursor, sched_start_date, interval)
    db.commit(conn)    
    conn.close()
    
    print("Added new tweet group with gid {}".format(result))
    
    header = {"Content-Type": "application/json"}
    res = HTTPResponse(status=200, body=json.dumps({'gid': result}), headers=header)    
    return res

@route('/api/1.0/update_tweet_group.json', method=["POST"])
def api_update_tweet_group():
    print("Content-Type: {}".format(request.get_header))
    body = request.json
    print(body)

    gid = body['gid']
    sched_start_date = body['sched_start_date']
    interval = body['interval']
    status = body['status']

    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    result = db.update_tweet_group(conn, cursor, gid, sched_start_date, interval, status)
    conn.close()
    print("Updated the tweet group with gid: {}, sched_start_date: {}, interval: {}, status: {}".format(gid, sched_start_date, interval, status))

    header = {"Content-Type": "application/text"}
    res = HTTPResponse(status=200, headers=header)    
    return res


@route('/api/1.0/search_tweet_groups_by_date', method=["POST"])
def api_search_tweet_groups_by_date():
    print("Content-Type: {}".format(request.get_header))
    body = request.json
    print(body)
    
    date = body["date"]
    
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    # cursor.execute("SELECT * FROM sched_tweet_groups")
    result = db.search_group_by_date(cursor, date)
    # import pdb; pdb.set_trace()
        
    conn.close()

    header = {"Content-Type": "application/json"}
    res = HTTPResponse(status=200, body=json.dumps(result), headers=header)    
    return res

@route('/api/1.0/delete_tweet_group.json', method=["POST"])
def api_delete_tweet_group():
    body = request.json

    gid = body['gid']
    
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    result = db.del_group(cursor, gid)
    db.commit(conn)    
    conn.close()
    
    print("Deleted the tweet group with gid {}".format(result))
    
    header = {"Content-Type": "application/text"}
    res = HTTPResponse(status=200, headers=header)    
    return res

# 廃止する？ -> update_tweet.json に統合
@route('/api/1.0/add_tweet.json', method=["POST"])
def api_add_tweet():
    body = request.json

    gid = body['gid']
    subid = body['subid']
    text = body['text']
    
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    result = db.add_tweet(cursor, gid, subid, text)
    
    db.commit(conn)    
    conn.close()
    
    print("Added new tweet with gid {}, subid {}, and text {}".format(result, subid, text))
    
    header = {"Content-Type": "application/json"}
    res = HTTPResponse(status=200, body=json.dumps({'id': result}), headers=header)    
    return res

@route('/api/1.0/update_tweet.json', method=["POST"])
def api_update_tweet():
    # 新規登録、更新を兼ねる。
    # 新規登録：id未定義で判定。gid, subid, text が必須。idを採番して返す。
    # 更新：id定義で判定。textが必須。git, subidはペアで定義されていれば、その値で更新。

    req_error = False;
    body = request.json

    # 入力のチェック
    try:
        id = body['id']
        new_tweet = False;
    except KeyError:
        new_tweet = True;    

    try:
        text = body['text']
    except KeyError:
        req_error = True;
        
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
        
    if new_tweet == True:  # 新規登録
        try:
            gid = body['gid']
        except KeyError:
            req_error = True;
        try:
            subid = body['subid']
        except KeyError:
            req_error = True;
        
        id = db.add_tweet(cursor, gid, subid, text)  # return gid
        print("Added new tweet {} with gid {}, subid {}, and text {}".format(id, gid, subid, text))
        
    else:  # 更新
        id = db.update_tweet(cursor, id, text)
        print("Updated the tweet with id {}, and text {}".format(id, text))
            
    db.commit(conn)
    conn.close()
    
    header = {"Content-Type": "application/json"}
    res = HTTPResponse(status=200, body=json.dumps({'id': id}), headers=header)    
    return res


@route('/api/1.0/search_tweets_by_gid.json', method=["POST"])
def api_search_tweets_by_gid():
    print("Content-Type: {}".format(request.get_header))
    body = request.json
    print(body)
    
    gid = body["gid"]
    
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    # cursor.execute("SELECT * FROM sched_tweet_groups")
    result = db.search_tweets_by_gid(cursor, gid)
    import pdb; pdb.set_trace()
        
    conn.close()
    
    print("Search tweets with gid {}.".format(gid))

    header = {"Content-Type": "application/json"}
    res = HTTPResponse(status=200, body=json.dumps(result), headers=header)    
    return res


@route('/api/1.0/delete_tweet.json', method=["POST"])
def api_delete_tweet():
    body = request.json

    id = body['id']
    
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    db.del_tweet(cursor, id)
    db.commit(conn)
    conn.close()
    
    print("Deleted the tweet with id {}".format(id))
    
    header = {"Content-Type": "application/json"}
    res = HTTPResponse(status=200, body=json.dumps({'id': id}), headers=header)    
    return res

@route('/scripts/<name>')
def scripts(name):
    
    return template('scripts/' + name)
    
run(host='0.0.0.0', port=8081, debug=True)
