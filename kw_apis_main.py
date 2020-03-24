# -*- coding:utf-8 -*-
from bottle import request, HTTPResponse
import json
import twitter_client as tc
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

    res_body = {'gid': result}
    return res_body

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

    res_body = {}
    return res_body

def search_tweet_groups_by_date(request):

    print("Content-Type: {}".format(request.get_header))
    body = request.json
    print(body)

    date = body["date"]

    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    # cursor.execute("SELECT * FROM sched_tweet_groups")
    result = db.search_group_by_date(cursor, date)
    conn.close()

    res_body = result
    return res_body

def delete_tweet_group(request):

    body = request.json

    gid = body['gid']

    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    result = db.del_group(cursor, gid)
    db.commit(conn)    
    conn.close()

    print("Deleted the tweet group with gid {}".format(result))

    res_body = {'gid': result }
    return res_body

def update_tweet(request):
    # Tweet(RT, 画像付TweetもTweetとして取り扱う) 新規登録・更新用API。
    # ポストされるデータのidの定義の有無で新規または更新を判定。
    # 新規登録：
    #   id未定義の場合。rt_flagが必須(0: tweet, 1: RT)
    #   gid(推奨 default=0), subid(推奨 default=0), text(推奨 default='')、org_tweet_id(推奨 default=0) 。
    #   idを採番して返す。
    # 更新：
    #   id定義の場合。rt_flagが必須(0: tweet, 1: RT)
    #   tweetの場合、text、retweetの場合、org_tweet_idが推奨（ブランクの場合は空欄または0で更新される）
    #   gid, subidは無視。

    ## Session ID認証成功の場合のメイン処理
    req_error = False;
    body = request.json

    # 入力のチェック
    try:
        id = body['id']
        new_tweet = False;
    except KeyError:
        new_tweet = True;

    # rt_flag (必須)
    try:
        rt_flag = int(body['rt_flag'])
    except KeyError:
        req_error = True;


    if rt_flag == 1:
        try:
            org_tweet_id = body['org_tweet_id']
        except KeyError:
            org_tweet_id = 0;
    elif rt_flag == 0:
        try:
            text = body['text']
        except KeyError:
            text = '';

    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)

    if new_tweet == True:  # 新規登録
        try:
            gid = body['gid']
        except KeyError:
            gid = 0;

        try:
            subid = body['subid']
        except KeyError:
            subid = 0;

        if rt_flag == 0:
            id = db.add_tweet(cursor, gid, subid, text)  # return gid
            print("Added new tweet {} with gid {}, subid {}, and text {}".format(id, gid, subid, text))
        elif rt_flag == 1:
            # Retweet対象のtweetのテキストを取得
            twitter = tc.twitter_auth()
            res = tc.get_tweet(twitter, org_tweet_id)
            org_tweet_text = 'Blank'
            if res.status_code == 200:
                tweet = json.loads(res.text)
                org_tweet_text = tweet['text'] + ' by ' + tweet['user']['name'] + ' at ' + tweet['created_at']

            id = db.add_retweet(cursor, gid, subid, org_tweet_id, org_tweet_text)
            print("Added new retweet {} with gid {}, subid {}, and org_tweet_id {} ({})".format(id, gid, subid, org_tweet_id, org_tweet_text))
    else:  # 更新
        if rt_flag == 0:
            id = db.update_tweet(cursor, id, text)
            print("Updated the tweet with id {}, and text {}".format(id, text))
        elif rt_flag == 1:
            # Retweet対象のtweetのテキストを取得
            twitter = tc.twitter_auth()
            res = tc.get_tweet(twitter, org_tweet_id)
            org_tweet_text = 'Blank'
            if res.status_code == 200:
                tweet = json.loads(res.text)
                org_tweet_text = tweet['text'] + ' by ' + tweet['user']['name'] + ' at ' + tweet['created_at']
            id = db.update_retweet(cursor, id, org_tweet_id, org_tweet_text)
            print("Updated the retweet with id {}, and org_tweet_id {}({})".format(id, org_tweet_id, org_tweet_text))

    db.commit(conn)
    conn.close()

    res_body = {'id': id}
    if rt_flag == 1:
        res_body['org_tweet_text'] = org_tweet_text

    return res_body


def search_tweets_by_gid(request):
    
    print("Content-Type: {}".format(request.get_header))
    body = request.json
    print(body)

    gid = body["gid"]

    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    # cursor.execute("SELECT * FROM sched_tweet_groups")
    result = db.search_tweets_by_gid(cursor, gid)

    conn.close()

    print("Search tweets with gid {}.".format(gid))

    res_body = result
    return res_body


def delete_tweet(request):

    body = request.json

    id = body['id']

    conn = db.connect_db(dbname)
    cursor = db.get_cursor(conn)
    db.del_tweet(cursor, id)
    db.commit(conn)
    conn.close()

    print("Deleted the tweet with id {}".format(id))

    res_body = {'id': id}
    return res_body
