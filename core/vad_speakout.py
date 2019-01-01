# -*- coding: utf-8 -*-
# 多线程实现语音合成时，语句切割和语音切割

from core.speakout import tts_main_vad
from audioDeal import wav2pcm
import threading
import queue
import re
from setting import settings
from datetime import datetime
import time
import os
import shutil

queue = queue.Queue()
event = threading.Event()


def vadfile_creat(path):
    import stat
    # 初始化切割后的语音存放文件夹（清除文件夹下所有文件）
    def remove_readonly(func, path, _):  # 定义回调函数
        os.chmod(path, stat.S_IWRITE)  # 删除文件的只读属性
        func(path)
    if os.path.exists(path):
        shutil.rmtree(path, onerror=remove_readonly)  # 将整个文件夹删除
        os.makedirs(path)  # 创建一个文件夹
    else:
        os.makedirs(path)  # 没有文件夹就新建一个


class MakeData(threading.Thread):
    def __init__(self, respond_words):
        super().__init__()
        self.respond_words = respond_words

    def text_vad(self):
        # pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
        # test_text = 'b,b.b/b;b\'b`b[b]b<b>b?b:b"b{b}b~b!b@b#b$b%b^b&b(b)b-b=b_b+b，b。b、b；b‘b’b【b】b·b！b b…b（b）b'
        self.respond_words = str(self.respond_words)
        pattern = r'\.|;|\?|!|。|、|；|·|！| |…|（|）'
        result_list = re.split(pattern, self.respond_words)
        re_list = [x for x in result_list if x != '']
        print(re_list)
        return re_list  # 返回列表形式的数据


    def run(self):
        num_list = self.text_vad()
        vadfile_creat(settings.SPEACK_PATH)
        for i in num_list:
            dt = datetime.now()
            nowtime = dt.strftime("%Y%m%d%H%M%S%f")
            record_path = settings.SPEACK_PATH + nowtime + r".wav"  # 以时间命名
            tts_main_vad(i, record_path)
            queue.put(record_path)
        queue.put(-1)       # queue最后放进一个结束记号，方便写代码和判断情况


class HandleData(threading.Thread):

    def run(self):
        while True:
            data = queue.get()
            if data != -1:  # 结束标志queue.qsize()>0:
                # print('Get from queue.')
                wav2pcm.audio_play(data)
                del(data)

            else:
                print("queue empty")
                break



if __name__ == '__main__':

    respond_words = '这几天心里颇不宁静。今晚在院子里坐着乘凉，忽然想起日日走过的荷塘，在这满月的光里，总该另有一番样子吧。月亮渐渐地升高了，墙外马路上孩子们的欢笑，已经听不见了；'

    threads = [MakeData(respond_words), HandleData()]
    for t in threads:
        t.start()

    for t in threads:
        t.join()




