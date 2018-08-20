# coding: utf-8
import base64
from core.get_token import get_access_token
import urllib.request
import json


def baidu_asr(data, id, token):
    speech_data = base64.b64encode(data).decode("utf-8")
    speech_length = len(data)

    post_data = {
        "format": "pcm",
        "rate": 16000,
        "channel": 1,
        "cuid": id,
        "token": token,
        "speech": speech_data,
        "len": speech_length
    }
    url = "http://vop.baidu.com/server_api"
    json_data = json.dumps(post_data).encode("utf-8")
    json_length = len(json_data)
    # print(json_data)

    req = urllib.request.Request(url, data=json_data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Content-Length", json_length)

    print("asr start request\n")
    resp = urllib.request.urlopen(req)
    print("asr finish request\n")
    resp = resp.read()
    resp_data = json.loads(resp.decode("utf-8"))
    # print(resp_data)
    if resp_data["err_no"] == 0:
        return resp_data["result"]
    else:
        print(resp_data)
        return None


def asr_main(filename):
    f = open(filename, "rb")
    audio_data = f.read()
    f.close()

    token = get_access_token()
    ##    token = "以上获取token令牌可以保持下来，不用一直获取，一个月有效"
    uuid = "11561301"
    resp = baidu_asr(audio_data, uuid, token)
    print(resp)
    return resp
