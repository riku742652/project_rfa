import time, datetime
import json
import requests
from config import TIME_ZONE, PIXELA_USER, PIXELA_ID, PIXELA_TOKEN
from vision_api import call_vision_api
from twitter import getTweetUrl

def rfa():
    now = datetime.datetime.now(TIME_ZONE)
    # 最新のツイート画像URLを取得
    media_url = getTweetUrl(now)
    if not media_url:
        print("failed to get url.")
        return
    # Google Cloud Vision APIを叩く
    texts = call_vision_api(media_url)
    if not texts:
        print("failed to call google vision api.")
    text_list = texts.splitlines()
    print(text_list)
    calorie = ''
    mileage = ''
    for text in text_list:
        if "kcal" in text:
            calorie = text.replace("kcal", "")
            break
    else:
        print("can't recognize it properly.")
        return

    print("{} calorie: {}".format(now.strftime("%Y/%m/%d"),
                                               calorie,
                                               ))
    # PIXELA APIを叩く
    url_items = 'https://pixe.la/v1/users/{}/graphs/{}'.format(PIXELA_USER,
                                                               PIXELA_ID
                                                               )
    headers = {
        'X-USER-TOKEN': PIXELA_TOKEN
    }
    item_data = {
        'date': now.strftime("%Y%m%d"),
        'quantity': calorie,
    }

    res = requests.post(url_items, headers=headers, json=item_data)
    data = res.json()
    if not data.get("isSuccess"):
        print("pixela api post failed. reason: {}".format(data.get("message")))
        return
    print("data plot success.")
    return

if __name__ == "__main__":
    rfa()
