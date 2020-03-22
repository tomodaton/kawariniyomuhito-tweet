import urllib
import json, config
from requests_oauthlib import OAuth1Session
import db_create_tables as dbc

dbname = './example.db'
url_home = "https://api.twitter.com/1.1/statuses/home_timeline.json"  # home タイムライン
url_tl = "https://api.twitter.com/1.1/statuses/user_timeline.json" # 自アカウントのタイムライン
url_friends = "https://api.twitter.com/1.1/friends/list.json" 
url_post = "https://api.twitter.com/1.1/statuses/update.json" # ツイート
url_canceltweet_base = "https://api.twitter.com/1.1/statuses/destroy/"
url_retweet_base = "https://api.twitter.com/1.1/statuses/retweet/"
url_unretweet_base = "https://api.twitter.com/1.1/statuses/unretweet/"
url_search = "https://api.twitter.com/1.1/search/tweets.json"


def twitter_auth():
    twitter = OAuth1Session(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
    return twitter
    
def retweet(twitter, tweetId):
    url = url_retweet_base + "%s.json"%tweetId
    url = url_retweet_base + "%s.json"%tweetId
    res = twitter.post(url)
    print(res)
    return res
    
def unretweet(twitter, tweetId):
    url = url_unretweet_base + "%s.json"%tweetId
    res = twitter.post(url)
    print(res)

def print_tl(res):
    if res.status_code == 200: # 正常
        timeline = json.loads(res.text)
        print('************************************************************************************************************************')
        for tweet in timeline:
            print(tweet['user']['name']+'::'+tweet['text'])
            print(tweet['created_at'])
            print(tweet['id'])
            print('************************************************************************************************************************')

    else: # 異常
        print("Failed: %d" % res.status_code)

def post_tweet(twitter, tweet):
    params = {"status": tweet}

    res = twitter.post(url_post, params =  params)

    print(res.text)
    print(json.loads(res.text))

    if res.status_code == 200:
        print("Success")
    else:
        print("Failed. :  %d" % res.status_code)
    return res
        
def cancel_tweet(twitter, tweetId):
    url = url_canceltweet_base + "%s.json"%tweetId
    res = twitter.post(url)
    print(res)

def search_tweet(word, count):
    params = {'q': word, 'count': count}
    print(url_search)
    print(params)
    res = twitter.get(url_search, params=params)
    timeline = json.loads(res.text)
    print('************************************************************************************************************************')
    for tweet in timeline['statuses']:
        print(tweet['user']['name']+'::'+tweet['text'])
        print(tweet['created_at'])
        print(tweet['id'])
        print('************************************************************************************************************************')

# Main Procedure
if __name__ == '__main__':
        
    twitter = OAuth1Session(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    while 1:
        print()
        print()
        mode = input('Home: 1, My tweets: 2, Tweet: 3, Cancel Tweet: 4, Retweet: 5, UnRetweet: 6, Search: 7, Exit: 9>> ')
        print(mode)

        if mode == '1':
            # タイムライン取得
            res = twitter.get(url_home)
            print_tl(res)
        elif mode == '2':
            res = twitter.get(url_tl)
            print_tl(res)
        elif mode == '3':
            print("ツイート内容を入力してください。")
            tweet = input('>> ')
            post_tweet(twitter, tweet) 
        elif mode == '4':
            print("削除するツイートのtweet IDを入力してください。")
            tweetId = input('>> ')
            cancel_tweet(twitter, tweetId) 
        elif mode == '5':
            print("リツイートするツイートのtweet IDを入力してください。")
            tweetId = input('>> ')
            retweet(twitter, tweetId) 
        elif mode == '6':
            print("リツイートを取り消すツイートのtweet IDを入力してください。")
            tweetId = input('>> ')
            unretweet(twitter, tweetId)
        elif mode == '7':
            print("検索キーワードを入力してください。")
            word = input('>> ')
            search_tweet(word, 100)
        elif mode == '24':
            date = input('date?>')
            conn = dbc.connect_db(dbname)
            cursor = dbc.get_cursor(conn)
            print(dbc.list_sched_tweets(cursor, date))
            
        elif mode == '9':
           exit()



