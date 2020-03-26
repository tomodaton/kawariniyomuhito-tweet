# -*- coding:utf-8 -*-
from bottle import route, run, request, response, HTTPResponse, default_app, static_file
from bottle import template
import json
import sqlite3
import db_create_tables as db
import time, datetime
import config
import hashlib
import twitter_client as tc
import kw_sessions as kw_s
import kw_util
import kw_apis_main

dbname = './example.db'
# dbname = './schetweet.db'


@route('/', method=['GET', 'POST'])
def index():

    login_status = kw_s.login(request)
    return template('index.tpl', login=login_status)


@route('/top.html', method='GET')
def top():

    # Session ID認証
    sessionid_valid = kw_s.authorize_sessionid(request)

    # Session ID認証成功
    if ( sessionid_valid == True ):
        pass
    # Session ID認証失敗
    else:
        return kw_util.generate_response_if_auth_failed()

    ## Session ID認証成功の場合のresponse生成
    # 1. 表示期間の生成
    from_date = request.query.get('from_date')
    to_date = request.query.get('to_date')
    dates = kw_util.generate_dates(from_date, to_date)

    # 2. 表示ツイートの抽出
    #  DBアクセス
    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)

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
@route('/api/1.0/<uri>', method=["POST"])
def api_universal(uri):

    # Session ID認証
    sessionid_valid = kw_s.authorize_sessionid(request)

    # Session ID認証成功
    if ( sessionid_valid == True ):
        # Session ID認証成功の場合の各API Main処理
        if uri == 'add_tweet_group.json': # Tweet Group追加API
            res_body = kw_apis_main.add_tweet_group(request)
        elif uri == 'update_tweet_group.json':  # Tweet Group更新API
            res_body = kw_apis_main.update_tweet_group(request)
        elif uri == 'search_tweet_groups_by_date': # Tweet Group 検索(by date, by gid)
            res_body = kw_apis_main.search_tweet_groups_by_date(request)
        elif uri == 'delete_tweet_group.json': # Tweet Group 削除
            res_body = kw_apis_main.delete_tweet_group(request)
        elif uri == 'update_tweet.json': # Tweet追加・更新
            res_body = kw_apis_main.update_tweet(request)
        elif uri == 'search_tweets_by_gid.json': # Tweet検索
            res_body = kw_apis_main.search_tweets_by_gid(request)
        elif uri == 'delete_tweet.json': # Tweet削除
            res_body = kw_apis_main.delete_tweet(request)
        # Response
        return kw_util.generate_api_response(res_body)

    # Session ID認証失敗
    else:
        return kw_util.generate_api_response_if_auth_failed()

@route('/scripts/<name>')
def scripts(name):

    # Session ID認証
    sessionid_valid = kw_s.authorize_sessionid(request)

    # Session ID認証成功
    if ( sessionid_valid == True ):
        return static_file(name, root='./scripts')
    # Session ID認証失敗
    else:
        return kw_util.generate_api_response_if_auth_failed()

    
if __name__ == '__main__':
    run(host='0.0.0.0', port=80, debug=True)
else:
    application= default_app()