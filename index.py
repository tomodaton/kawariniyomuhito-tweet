# -*- coding:utf-8 -*-
from bottle import route, run, request, HTTPResponse
from bottle import template
import json
import sqlite3
import db_create_tables as db
import time, datetime


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



@route('/')
def index():
    name = "代わりに読む人"
    return template('index.tpl', name=name)

@route('/top.html', method='GET')
def top():

    from_date = request.query.get('from_date')
    to_date = request.query.get('to_date')
            
    dates = generate_dates(from_date, to_date)

    # DBアクセス
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)

    groups = {}
    tweets = {}
    for date in dates:
        results = db.search_group_by_date(cursor, date)
        groups[date]= results
        for group in results:
            tweets[group['gid']] = db.search_tweets_by_gid(cursor, group['gid'])
    print(tweets)
    db.close_db(conn)
            
    return template('top.tpl', dates=dates, groups=groups, tweets=tweets)


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
    body = request.json

    id = body['id']
    text = body['text']
    
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    db.update_tweet(cursor, id, text)
    
    db.commit(conn)    
    conn.close()
    
    print("Updated the tweet with id {}, and text {}".format(id, text))
    
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




run(host='0.0.0.0', port=8081, debug=True)
