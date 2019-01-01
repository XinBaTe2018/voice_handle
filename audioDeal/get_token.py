# -*- coding: utf-8 -*-
'''
@auther: Liruijuan
@summary: 得到百度语音和人脸识别api接口许可
'''
from urllib import request, parse
import json
from setting import settings

def get_voice_access_token():
    url = "https://openapi.baidu.com/oauth/2.0/token"
    grant_type = settings.Grant_type
    client_id = settings.Client_id
    client_secret = settings.Client_secret
    url = url + "?" + "grant_type=" + grant_type + "&" + "client_id=" + client_id + "&" + "client_secret=" + client_secret
    resp = request.urlopen(url).read()
    data = json.loads(resp.decode("utf-8"))
    return data["access_token"]

def get_face_access_token():
    host = "https://aip.baidubce.com/oauth/2.0/token"
    grant_type = settings.Grant_type
    client_id = settings.Client_id
    client_secret = settings.Client_secret
    host = host + "?" + "grant_type=" + grant_type + "&" + "client_id=" + client_id + "&" + "client_secret=" + client_secret
    req= request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    content = request.urlopen(host).read()
    content = bytes.decode(content)
    # 转化为字典
    content = eval(content[:-1])
    # print(content)
    return content['access_token']

if __name__ == '__main__':
    get_face_access_token()