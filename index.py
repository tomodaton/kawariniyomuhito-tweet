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
def greet():
    name = "hoge"
    return template('index.tpl', name=name)

@route('/top.html', method='GET')
def top():
    print(request.query.fromdate)

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

    
    print()
    print()
    for key in groups.keys():
        print(key)
            
    return template('top.tpl', dates=dates, groups=groups, tweets=tweets)

@route('/api/1.0/update_tweet_group.json', method=["POST"])
def api_update_tweet_group():
    print("Content-Type:")
    print(request.get_header("Content-Type"))
    body = request.json
    print(body)
    gid = body['gid']
    sched_start_date = body['sched_start_date']
    status = body['status']

    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    result = db.update_tweet_group(conn, cursor, gid, sched_start_date, status)
    conn.close()

    header = {"Content-Type": "application/json"}
    res = HTTPResponse(status=200, result=json.dumps({"test": 100}), headers=header)    
    return res

@route('/api/1.0/add_tweet_group.json', method=["POST"])
def api_add_tweet_group():
    body = request.json

    sched_start_date = body['sched_start_date']
    interval = body['interval']
    
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    result = db.add_group(conn, cursor, sched_start_date, interval)
    conn.close()
    

@route('/api/1.0/delete_tweet_group.json', method=["POST"])



@route('/api/1.0/search_gid', method=["POST"])
def api_search_gid():
    body = request.json
    date = body["date"]
    
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    # cursor.execute("SELECT * FROM sched_tweet_groups")
    db.search_group_by_date(cursor, date)
    result = ""
    for item in cursor.fetchall():
        result += str(item)
    
    conn.close()

    header = {"Content-Type": "application/json"}
    res = HTTPResponse(status=200, body=result, headers=header)    
    return res

run(host='0.0.0.0', port=8081, debug=True)
