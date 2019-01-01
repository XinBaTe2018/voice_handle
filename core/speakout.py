# -*- coding: utf-8 -*-
'''
@auther: Liruijuan
@summary: 使用百度api接口实现语音合成
'''
from audioDeal.get_token import get_voice_access_token
import urllib.request
from setting import settings
import os
import time
from datetime import datetime
import ssl


def baidu_tts_by_post(data, id, token):
    post_data = {
        "tex": data,
        "lan": "zh",
        "ctp": 1,
        "cuid": id,
        "aue": 6,   # 返回为二进制wav文件，查看百度API文档（3，4，5）各个含义
        "tok": token,
    }

    url = "http://tsn.baidu.com/text2audio"
    post_data = urllib.parse.urlencode(post_data).encode('utf-8')
    # print(post_data)
    req = urllib.request.Request(url, data=post_data)

    print("tts start request")
    resp = urllib.request.urlopen(req)
    print("tts finish request")
    resp = resp.read()
    return resp


def tts_main(words):
    token = get_voice_access_token()
    text = urllib.parse.quote(words)
    uuid = "11561301"
    resp = baidu_tts_by_post(text, uuid, token)

    # dt = datetime.now()
    # nowtime = dt.strftime("%Y%m%d%H%M%S%f")
    # record_path = settings.SPEACK_FILE + nowtime + r".wav"  # 以时间命名
    with open(settings.SPEACK_FILE, "wb") as f:
        f.write(resp)
        f.close()

def tts_main_vad(words, record_path):
    token = get_voice_access_token()
    text = urllib.parse.quote(words)
    uuid = "11561301"
    resp = baidu_tts_by_post(text, uuid, token)

    # dt = datetime.now()
    # nowtime = dt.strftime("%Y%m%d%H%M%S%f")
    # record_path = settings.SPEACK_FILE + nowtime + r".wav"  # 以时间命名
    with open(record_path, "wb") as f:
        f.write(resp)
        f.close()


if __name__ == '__main__':
    tts_main("环境和健康息息相关保护环境促进健康。")
