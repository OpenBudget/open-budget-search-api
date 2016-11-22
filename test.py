import json
import requests

data = json.loads(open("c:\\temp\\temp.txt", "r", encoding="utf-8").read())
requests.post("http://127.0.0.1:8888/index/exemption", json.dumps(data))
