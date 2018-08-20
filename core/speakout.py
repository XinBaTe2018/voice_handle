from core.get_token import get_access_token
import urllib.request
from setting import settings
import os


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
    token = get_access_token()
    text = urllib.parse.quote(words)
    uuid = "11561301"
    resp = baidu_tts_by_post(text, uuid, token)

    with open(settings.SPEACK_FILE, "wb") as f:
        f.write(resp)
        f.close()


if __name__ == '__main__':
    tts_main("环境和健康息息相关保护环境促进健康。")
