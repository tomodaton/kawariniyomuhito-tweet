# -*- coding:utf-8 -*-
from bottle import request, HTTPResponse
import json
import db_create_tables as db
import kw_apis_main

dbname = './example.db'
# dbname = './schetweet.db'


def add_tweet_group(request):
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

def update_tweet_group(request):
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