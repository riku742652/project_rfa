import json
import time
import requests
from config import PIXELA_USER, PIXELA_ID, PIXELA_TOKEN

manual_list = [
    {"date": "YYYYMMDD", "quantity": "00.00"},
]

url_items = 'https://pixe.la/v1/users/{}/graphs/{}'.format(PIXELA_USER,
                                                           PIXELA_ID
                                                           )
headers = {
    'X-USER-TOKEN': PIXELA_TOKEN
}

for index, item_data in enumerate(manual_list):
    res = requests.post(url_items, headers=headers, json=item_data)
    data = res.json()
    if not data.get("isSuccess"):
        print("pixela api post failed. reason: {}".format(data.get("message")))
        break
    print("{}/{} data plot success. response:{}".format(index+1, len(manual_list), data))
    time.sleep(5)