# -*- coding:utf-8 -*-
import time
import datetime
import twitter_client as tc
import db_create_tables as dbc


dbname = './example.db'

current_datetime = datetime.datetime.now()

twitter = tc.twitter_auth()
# tc.post_tweet(twitter, 'ただいま '+current_datetime)

# 開始時刻のTweet Groupを検索
current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Tweet GroupのTweetを抽出
conn = dbc.connect_db(dbname)
cursor = dbc.get_cursor(conn)
tweet_tuples = dbc.list_sched_tweets(conn, cursor, current_datetime)

# 抽出したtweetをtweet.
for tuple in tweet_tuples:
    # print(tuple)
    # print(dict(tuple))
    res = tc.post_tweet(twitter, tuple['text']+current_datetime)
    # res のSuccess/Failed をsched_tweetsに記録する。
    time.sleep(tuple['interval'])