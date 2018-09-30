# -*- coding: utf-8 -*-
'''
@auther: Liruijuan
@summary: 使用图灵机器人回答
'''
import requests
import json
from setting import settings


def TuLin(words):
    TuLin_API_KEY = settings.Tulin_API_KEY
    body = {"key": TuLin_API_KEY, "info": words.encode("utf-8")}
    url = "http://www.tuling123.com/openapi/api"
    r = requests.post(url, data=body, verify=True)
    if r:
        date = json.loads(r.text)
        return date["text"]
    else:
        return None
