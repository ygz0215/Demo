import requests
import json
def senddingding(params):
    url = "https://oapi.dingtalk.com/robot/send?access_token=6dd848fcae89391075f589fa75279e676fd03911d97eff7027595e08774e7f06"
    data = {
        "msgtype": "text",
        "text": {
        "content": params.get("content")
        },
    "at": {
    "atMobiles": params.get("atMobiles"),
    "isAtAll": params.get("isAtAll")
        }
    }
    headers = {
        'Content-type': 'application/json'
        }
    data = json.dumps(data)
    response = requests.post(url, headers=headers,data=data)
    print(response.content.decode())