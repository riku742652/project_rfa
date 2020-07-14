import time, datetime
import json
import pytz
from config import CONSUMER_KEY, CONSUMER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, TIME_ZONE, TWITTER_ACCOUNT
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
import vision_api

def convertToDate(str_date):
    t = time.strptime(str_date,'%a %b %d %H:%M:%S +0000 %Y')
    utc = pytz.timezone('UTC')
    d = datetime.datetime(*t[:6], tzinfo=utc)
    tm = d.astimezone(TIME_ZONE)
    zn = tm.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    ymd = tm.strftime('%Y-%m-%d')
    return tm

def getTweetUrl(now):
    CK = CONSUMER_KEY
    CS = CONSUMER_SECRET_KEY
    AT = ACCESS_TOKEN
    ATS = ACCESS_TOKEN_SECRET
    twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json" #タイムライン取得エンドポイント

    params = {'screen_name': TWITTER_ACCOUNT,
              'count': 1
            }

    res = twitter.get(url, params=params)

    if res.status_code == 200:
        data = json.loads(res.text)
        tweet_time = convertToDate(data[0]['created_at'])
        yesterday =  now - datetime.timedelta(days=1)
        is_media = True if data[0].get("extended_entities") else False

        # ツイート時間が実行日前日より後かつ画像付きツイートならURLを返す
        if  tweet_time > yesterday and is_media:
            return data[0]["extended_entities"]["media"][0]["media_url"]
        else:
            print("didn't do an RFA on {}.".format(now.strftime("%Y/%m/%d")))
            return False

    else:
        print("Failed: %d" % res.status_code)
        return False