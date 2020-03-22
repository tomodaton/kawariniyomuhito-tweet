import sqlite3
import json
import time, datetime
import config

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
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS sessions")
    cursor.execute("DROP TABLE IF EXISTS sched_tweets")
    cursor.execute("DROP TABLE IF EXISTS sched_tweet_groups")

    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)")
    cursor.execute("CREATE TABLE sessions (sessionid TEXT, expire TEXT)")
    cursor.execute("CREATE TABLE sched_tweets (id INTEGER PRIMARY KEY AUTOINCREMENT, gid INTEGER, subid INTEGER, text TEXT, rt_flag INTEGER, org_tweet_id INTEGER, tweet_id INTEGER, actual_date TEXT, status TEXT)")
    cursor.execute("CREATE TABLE sched_tweet_groups (gid INTEGER PRIMARY KEY AUTOINCREMENT,sched_start_date TEXT,interval INT,actual_start_date TEXT,status TEXT)")
    
def commit(conn):
    conn.commit()
    
def close_db(conn):
    conn.close()

# User/Session管理
def search_user_password(cursor, username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    item = cursor.fetchone()
    # print(str(dict(item)))

    if item != None:
        return True
    else:
        return False

def register_sessionid(cursor, sessionid):
    datetime_now = datetime.datetime.now()
    datetime_expire = datetime_now + datetime.timedelta(seconds=config.VALIDITY_PERIOD)
    cursor.execute("INSERT INTO sessions VALUES (?, ?)", (sessionid, datetime_expire))
    
def check_sessionid(cursor, sessionid):

    datetime_now = datetime.datetime.now()
    cursor.execute("SELECT * FROM sessions WHERE sessionid = ? AND expire > ?", (sessionid, datetime_now))
    result = cursor.fetchone()
    if result != None:
        print(dict(result))
        return True
    return False

def extend_validate_period(cursor, sessionid):
    datetime_now = datetime.datetime.now()
    new_datetime_expire = datetime_now + datetime.timedelta(seconds=config.VALIDITY_PERIOD)
    cursor.execute("UPDATE sessions SET expire = ? WHERE sessionid = ?", (new_datetime_expire, sessionid))

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
    result = cursor.execute("INSERT INTO sched_tweets(gid, subid, text, rt_flag, org_tweet_id, tweet_id, actual_date, status) VALUES (?, ?, ?, 0, '', '', '', 'DRAFT')", (gid, subid, text)).lastrowid
    return result

def update_tweet(cursor, id, text):
    cursor.execute("UPDATE sched_tweets SET text = ? WHERE id = ?", (text, id))
    cursor.execute("UPDATE sched_tweets SET rt_flag = 0, org_tweet_id = 0 WHERE id = ?", (id,))
    return id

def update_tweet_status(cursor, id, tweet_id, status):
    cursor.execute("UPDATE sched_tweets SET status = ?, tweet_id = ? WHERE id = ?", (status, tweet_id, id))
    
def del_tweet(cursor, id):
    cursor.execute("DELETE FROM sched_tweets WHERE id=?", (id,))

def search_tweets_by_date(conn, cursor, date):
    cursor.execute("SELECT sched_tweet_groups.gid, sched_tweet_groups.sched_start_date, sched_tweet_groups.interval, sched_tweet_groups.status, sched_tweets.id, sched_tweets.subid, sched_tweets.text, sched_tweets.rt_flag, sched_tweets.org_tweet_id FROM sched_tweet_groups INNER JOIN sched_tweets ON sched_tweet_groups.gid = sched_tweets.gid WHERE sched_tweet_groups.sched_start_date <= ?" , (date,))
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

# Retweet操作(登録更新以外(Delete/Update_status)はTweet操作で実行可能)
def add_retweet(cursor, gid, subid, org_tweet_id):

    result = cursor.execute("INSERT INTO sched_tweets(gid, subid, text, rt_flag, org_tweet_id, tweet_id, actual_date, status) VALUES (?, ?, '', 1, ?, '', '', 'DRAFT')", (gid, subid, org_tweet_id)).lastrowid
    return result

def update_retweet(cursor, id, org_tweet_id):
    cursor.execute("UPDATE sched_tweets SET org_tweet_id = ? WHERE id = ?", (org_tweet_id, id))
    cursor.execute("UPDATE sched_tweets SET rt_flag = 1, text = '' WHERE id = ?", (id,))
    return id


# 日付を指定して予約後のツイートを抽出（自動tweetプログラム側から呼び出し）
def list_sched_tweets(conn, cursor, datetime_s):
    cursor.execute("SELECT sched_tweet_groups.gid, sched_tweet_groups.sched_start_date, sched_tweet_groups.interval, sched_tweet_groups.status, sched_tweets.id, sched_tweets.subid, sched_tweets.text, sched_tweets.rt_flag, sched_tweets.org_tweet_id FROM sched_tweet_groups INNER JOIN sched_tweets ON sched_tweet_groups.gid = sched_tweets.gid WHERE sched_tweet_groups.sched_start_date <= ? AND sched_tweet_groups.status = 'SCHED'" , (datetime_s,))
    result = cursor.fetchall()
    # for row in result:
    #     print(json.dumps(dict(row)))
    return result

def search_scheduled_tweet_groups(conn, cursor, datetime_s):
    cursor.execute("SELECT gid, interval FROM sched_tweet_groups WHERE sched_start_date <= ? AND status = 'SCHEDULED'", (datetime_s,))
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
        mode = input('Init: 0, Show Tables: 01, Add/Show Users: 02/03, Add/Show Sessions: 05/06, Add/Show/Search/Delete Group: 11/12/13/19, Add/Show/Update/Delete Tweet: 21/22/23/24, Add/Show/Update/Detete Retwwet: 25/26/27/28, Search Tweets/Scheduled Tweets: 31/32, Set Scheduled: 40, Exit: 9>> ')
        print(mode)

        if mode == '0':
            create_tables(cursor)
            conn.commit()
        elif mode == '01':
            cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
            for item in cursor.fetchall():
                print(item)
        elif mode == '02':
            username = input('username >>')
            password = input('password >>')
            cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
            cursor.execute("SELECT * FROM users")
            for item in cursor.fetchall():
                print(dict(item))
        elif mode == '03':
            cursor.execute("SELECT * FROM users")
            for item in cursor.fetchall():
                print(dict(item))
        elif mode == '05':
            sessionid = input('sessionid >>')
            expire = input('expire >>')
            cursor.execute("INSERT INTO sessions VALUES (?, ?)", (sessionid, expire))
            conn.commit()
            cursor.execute("SELECT * FROM sessions")
            for item in cursor.fetchall():
                print(dict(item))
        elif mode == '06':
            cursor.execute("SELECT * FROM sessions")
            for item in cursor.fetchall():
                print(dict(item))
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
            text = input('text >>')
            update_tweet(cursor, id, text)
            conn.commit()
        elif mode == '24':
            id = input('id >>')
            del_tweet(cursor, id)
            conn.commit()

        elif mode == '25':
            gid = input('gid >>')
            subid = input ('subid >>')
            org_tweet_id = input('Tweet ID to retweet >>')
            add_retweet(cursor, gid, subid, org_tweet_id)
            conn.commit()
        elif mode == '26':
            cursor.execute("SELECT * FROM sched_tweets")
            for item in cursor.fetchall():
                print(item)
                print(dict(item))
        elif mode == '27':
            id = input('id >>')
            org_tweet_id = input('Tweet ID to retweet >>')
            update_retweet(cursor, id, org_tweet_id)
            conn.commit()
        elif mode == '28':
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
