# -*- coding:utf-8 -*-
import time
import datetime
import twitter_client as tc
import db_create_tables as dbc
import json


dbname = './example.db'

current_datetime = datetime.datetime.now()

twitter = tc.twitter_auth()
# tc.post_tweet(twitter, 'ただいま '+current_datetime)

# 開始時刻のTweet Groupを検索
current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Tweet GroupのTweetを抽出
conn = dbc.connect_db(dbname)
cursor = dbc.get_cursor(conn)


gids = []
intervals = {}
tweets = {}

# import pdb; pdb.set_trace()
groups = dbc.search_scheduled_tweet_groups(conn, cursor, current_datetime)
for tuple in groups:
    gids.append(tuple['gid'])
    intervals[tuple['gid']] = tuple['interval']

print(gids)

for gid in gids:
    tweets[gid] = dbc.search_tweets_by_gid(cursor, gid)
    print(tweets)
dbc.close_db(conn)


# 抽出したtweetをtweet.
for gid in gids:
    for tuple in tweets[gid]:
        # Tweet処理
        # res = tc.post_tweet(twitter, tuple['text']+current_datetime)
        res = tc.post_tweet(twitter, tuple['text'])
        # res = tc.post_tweet(twitter, tuple['text']+current_datetime)
        status_code = res.status_code
        tweet_id = json.loads(res.text)['id']

        # 結果の記録
        # res のSuccess/Failed を個々のsched_tweetsに記録する。
        if status_code == 200:
            status = "SUCCESS"
        else:
            status = "FAILED"        
        conn = dbc.connect_db(dbname)
        cursor = dbc.get_cursor(conn)
        # 記録のDBへの保存
        dbc.update_tweet_status(cursor, tuple['id'], tweet_id, status)
        dbc.commit(conn)
        dbc.close_db(conn)
        time.sleep(intervals[gid])
        # time.sleep(10)
    # 
    conn = dbc.connect_db(dbname)
    cursor = dbc.get_cursor(conn)
    dbc.update_tweet_group_status(conn, cursor, gid, "DONE")
    dbc.close_db(conn)
