# -*- coding: utf-8 -*-
'''
@auther: Liruijuan
@summary: 得到百度语音api接口许可
'''
import urllib.request
import json
from setting import settings


def get_access_token():
    url = "https://openapi.baidu.com/oauth/2.0/token"
    grant_type = settings.Grant_type
    client_id = settings.Client_id
    client_secret = settings.Client_secret
    url = url + "?" + "grant_type=" + grant_type + "&" + "client_id=" + client_id + "&" + "client_secret=" + client_secret
    resp = urllib.request.urlopen(url).read()
    data = json.loads(resp.decode("utf-8"))
    return data["access_token"]
