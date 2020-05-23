import json
import time
import requests
from config import PIXELA_USER, PIXELA_ID, PIXELA_TOKEN

delete_date = [
    "YYYYMMDD",
]

url_items = 'https://pixe.la/v1/users/{}/graphs/{}/'.format(PIXELA_USER,
                                                              PIXELA_ID
                                                              )
headers = {
    'X-USER-TOKEN': PIXELA_TOKEN
}

for index, date in enumerate(delete_date):
    url = url_items + date
    res = requests.delete(url, headers=headers)
    data = res.json()
    if not data.get("isSuccess"):
        print("pixela api post failed. reason: {}".format(data.get("message")))
        break
    print("{}/{} data delete success. response:{}".format(index+1, len(delete_date), data))
    time.sleep(5)