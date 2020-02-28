import sqlite3
import json
import time, datetime

dbname = './example.db'
# dbname = './schetweet.db'

# DB設定、接続関連 
def connect_db(dbname):
    return sqlite3.connect(dbname)

def get_cursor(conn):
    conn.row_factory = sqlite3.Row
    return conn.cursor()

def create_tables(cursor):
    # Create Tables
    cursor.execute("DROP TABLE IF EXISTS sched_tweets")
    cursor.execute("DROP TABLE IF EXISTS sched_tweet_groups")
    cursor.execute("CREATE TABLE sched_tweets (id INTEGER PRIMARY KEY AUTOINCREMENT, gid INTEGER, subid INTEGER, text TEXT, tweet_id INTEGER, actual_date TEXT, status TEXT)")
    cursor.execute("CREATE TABLE sched_tweet_groups (gid INTEGER PRIMARY KEY AUTOINCREMENT,sched_start_date TEXT,interval INT,actual_start_date TEXT,status TEXT)")
    
def commit(conn):
    conn.commit()
    
def close_db(conn):
    conn.close()

# Tweet Group操作
def add_group(cursor, sched_start_date, interval):
    # import pdb; pdb.set_trace()
    result = cursor.execute("INSERT INTO sched_tweet_groups(sched_start_date,interval,actual_start_date,status) VALUES (?, ?,'2099-12-31 23:59', 'DRAFT')", (sched_start_date, interval)).lastrowid
    return result;

def search_group_by_date(cursor, date):
    # cursor.execute("SELECT * FROM sched_tweet_groups WHERE sched_start_date >= datetime(date(?)", from_date, to_date);
    from_time = datetime.datetime.strptime(date, '%Y-%m-%d')
    to_time = datetime.datetime.strptime(date, '%Y-%m-%d')+datetime.timedelta(days=1, seconds=-1)
    cursor.execute("SELECT * FROM sched_tweet_groups WHERE sched_start_date >= ? AND sched_start_date <= ? ORDER BY sched_start_date ASC", (from_time, to_time));
    result = cursor.fetchall()
    groups = []
    for row in result:
        groups.append(dict(row)) 
    return groups
    
def search_group_by_gid():
    skip

def del_group(cursor, gid):
    cursor.execute("DELETE FROM sched_tweet_groups WHERE gid=?", (gid,))

def confirm_group(cursor, gid):
    cursor.execute("UPDATE sched_tweet_groups SET status = 'SCHEDULED' WHERE gid = ?", (gid,))

# Tweet操作
def add_tweet(cursor, gid, subid, text):
    result = cursor.execute("INSERT INTO sched_tweets(gid, subid, text, tweet_id, actual_date, status) VALUES (?, ?, ?, '', '', 'DRAFT')", (gid, subid, text)).lastrowid
    return result

def update_tweet(cursor, id, text):
    cursor.execute("UPDATE sched_tweets SET text = ? WHERE id = ?", (id, text))
    return id

def update_tweet_status(cursor, id, tweet_id, status):
    cursor.execute("UPDATE sched_tweets SET status = ?, tweet_id = ? WHERE id = ?", (status, tweet_id, id))
    
def del_tweet(cursor, id):
    cursor.execute("DELETE FROM sched_tweets WHERE id=?", (id,))

def search_tweets_by_date(conn, cursor, date):
    cursor.execute("SELECT sched_tweet_groups.gid, sched_tweet_groups.sched_start_date, sched_tweet_groups.interval, sched_tweet_groups.status, sched_tweets.id, sched_tweets.subid, sched_tweets.text FROM sched_tweet_groups INNER JOIN sched_tweets ON sched_tweet_groups.gid = sched_tweets.gid WHERE sched_tweet_groups.sched_start_date <= ?" , (date,))
    # import pdb; pdb.set_trace()
    result = cursor.fetchall()
    for row in result:
        print(dict(row))
    return result

def search_tweets_by_gid(cursor, gid):
    # import pdb; pdb.set_trace()
    cursor.execute("SELECT * FROM sched_tweets WHERE gid = ?", (gid, ));
    result = cursor.fetchall()
    tweets = []
    for row in result:
        tweets.append(dict(row)) 
    return tweets

# 日付を指定して予約後のツイートを抽出（自動tweetプログラム側から呼び出し）
def list_sched_tweets(conn, cursor, datetime_s):
    cursor.execute("SELECT sched_tweet_groups.gid, sched_tweet_groups.sched_start_date, sched_tweet_groups.interval, sched_tweet_groups.status, sched_tweets.id, sched_tweets.subid, sched_tweets.text FROM sched_tweet_groups INNER JOIN sched_tweets ON sched_tweet_groups.gid = sched_tweets.gid WHERE sched_tweet_groups.sched_start_date <= ? AND sched_tweet_groups.status = 'SCHED'" , (datetime_s,))
    # import pdb; pdb.set_trace()
    result = cursor.fetchall()
    # for row in result:
    #     print(json.dumps(dict(row)))
    return result

def search_scheduled_tweet_groups(conn, cursor, datetime_s):
    cursor.execute("SELECT gid FROM sched_tweet_groups WHERE sched_start_date <= ? AND status = 'SCHEDULED'", (datetime_s,))
    result = cursor.fetchall()
    return result

# For API
# Tweet Group更新
def update_tweet_group(conn, cursor, gid, sched_start_date, interval, status):
    cursor.execute("UPDATE sched_tweet_groups SET sched_start_date=?, status=?, interval=? WHERE gid=?", (sched_start_date, status, interval, gid))
    commit(conn)
    return 200;

def update_tweet_group_status(conn, cursor, gid, status):
    cursor.execute("UPDATE sched_tweet_groups SET status=? WHERE gid=?", (status, gid))
    commit(conn)

def add_tweet_group(cursor, sched_start_date, status):
    result = add_group(cursor, sched_start_date, status)
    return result


# CUI実行時
if __name__ == '__main__':

    conn = connect_db(dbname)
    cursor = get_cursor(conn)

    while 1:
        print()
        print()
        mode = input('Init: 0, Show Tables: 01, Add/Show/Search/Delete Group: 11/12/13/19, Add/Show/Delete Tweet: 21/22/23, Search Tweets/Scheduled Tweets: 31/32, Set Scheduled: 40, Exit: 9>> ')
        print(mode)

        if mode == '0':
            create_tables(cursor)
            conn.commit()
        elif mode == '01':
            cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
            for item in cursor.fetchall():
                print(item)
        elif mode == '11': # Tweet Group追加
            sched_start_date = input('Start Date>>')
            result = add_group(cursor, sched_start_date, 1)
            print(result)
            conn.commit()
        elif mode == '12': # Tweet Group一覧取得
            cursor.execute("SELECT * FROM sched_tweet_groups")
            for item in cursor.fetchall():
                print(item)
                print(dict(item))
                # print(json.dumps(item))
        elif mode == '13': # Tweet Group検索
            date = input('Date >>')
            print(search_group_by_date(cursor,date))
        elif mode == '14': # Tweet Group更新
            gid = input('gid >>')
            sched_start_date = input('sched_start_date >>')
            interval = input('interval >>')
            status = input('status >>')
            update_tweet_group(conn, cursor, gid, sched_start_date, interval, status)
        elif mode == '19': # Tweet Group削除
            gid = input('gid >>')
            del_group(cursor, gid)
            conn.commit()
        elif mode == '21':
            gid = input('gid >>')
            subid = input ('subid >>')
            text = input('Body of Tweet >>')
            add_tweet(cursor, gid, subid, text)
            conn.commit()
        elif mode == '22':
            cursor.execute("SELECT * FROM sched_tweets")
            for item in cursor.fetchall():
                print(item)
                print(dict(item))
        elif mode == '23':
            id = input('id >>')
            del_tweet(cursor, id)
            conn.commit()
        elif mode == '31':
            date = input('date >>')
            cursor = get_cursor(conn)
            print(search_tweets_by_date(conn, cursor, date))
            for tweet in list_sched_tweets(conn, cursor, date):
                print(tweet)
        elif mode == '32':
            date = input('date >>')
            cursor = get_cursor(conn)
            print(list_sched_tweets(conn, cursor, date))
            for tweet in list_sched_tweets(conn, cursor, date):
                print(tweet)
        elif mode == '40':
            gid = input('gid >>')
            confirm_group(cursor, gid)
            conn.commit()
        elif mode == '9':
            conn.close()
            exit()
