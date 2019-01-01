# -*- coding: utf-8 -*-
'''
@auther: Liruijuan & Liyaguo
@summary: 运行的主程序，主要实现检测录音 + 语音识别 + 核心机器人回答 + 语音合成
'''
from audioDeal import wav2pcm
import os, time
from core.MyRobert import bot, MyThread
from core.TuLinRobert import TuLin
from core.speakout import tts_main
from setting import settings
from core.sound2wordBD import asr_main     # 该文档使用讯飞api进行语音识别
from core.sound2wordXF import wordfromS
from core.moni_record import Monitor
from core.unknow_question_save import UnQuetion
from core.conversation_save import ConversationSaved
from core.speakerID import SpeakerID
import threading
from time import sleep

import re
import random


class XbtBot():
    def __init__(self):
        self.words = None
        self.response = None
        self.results = None
        self.name = None

    def record_audio(self):  # 检测声音，进行录音
        monitor = Monitor()
        res = monitor.monitor() # 检测声音，如果超过阈值则为True
        if res:
            monitor.record()
            monitor.write_audio_to_wave(settings.LISTEN_FILE)
    '''
    #声纹模块
    def speakerid(self):
        speakerid = SpeakerID()
        conversation = ConversationSaved.conndb()
        t_speakerid = MyThread(speakerid.run_readFromAudioFile, args=())
        t_speakerid.start()
        t_speakerid.join()
        res = t_speakerid.get_result()  # 判断是否存储到声纹库
        if res:
            self.name = speakerid.match_name
            t_append = MyThread(conversation.append, args=(self.words, self.name))
            t_append.start()
        else:
            self.name = speakerid.name
            t_dump = MyThread(conversation.dump, args=(self.words, self.name))
            t_dump.start()
    '''
    def voice2word(self):
        start1 = time.time()
        self.words = wordfromS(settings.LISTEN_FILE)  # 读取录音文件，通过讯飞API实现语音转写
        stop1 = time.time()
        print("讯飞API:%s" % (stop1 - start1))

    def think(self):
        start2 = time.time()
        chatterbot_respone = bot.get_response(self.words)
        response = chatterbot_respone
        print(response)
        t = MyThread(TuLin, args=(self.words,))
        t.setDaemon(True)
        t.start()
        if response !='False':
            self.response =response
            print("Mybot-{}".format(self.response))
        else:
            t.join()
            self.response = t.get_result()
            self.record()
            print("tulin-{}".format(self.response))

        stop2 = time.time()
        print("思考时间:%s" % (stop2 - start2))

    def record(self):
        s=UnQuetion.conndb()
        t1 = MyThread(s.dump, args=(self.words,))
        t1.start()

    def word2vice(self):
        start3 = time.time()
        tts_main(str(self.response))
        stop3 = time.time()
        wav2pcm.audio_play(settings.SPEACK_FILE)
        print("语音合成时间%s" % (stop3 - start3))
        # t1 = MyThread(wav2pcm.audio_play, args=(str(settings.SPEACK_FILE),))
        # wav2pcm.audio_play(settings.SPEACK_FILE)
        # t1.start()

    def run(self):
        while True:
            try:
                self.record_audio()
                # self.speakerid()
                self.voice2word()
                if self.words == None:
                    tts_main("不好意思，您可以再说一遍吗？")
                    wav2pcm.audio_play(settings.SPEACK_FILE)
                else:
                    self.results = re.findall(r'(再见|goodbye|bye bye|拜拜|退出|再会|待会见|张总|李总|王总|赵总|刘总|马总)', self.words)
                    if len(self.results) == 0:
                        self.think()
                        self.word2vice()
                    elif [x for x in self.results if x in ["张总", "王总", "李总", "赵总", "刘总","马总"]]:
                        words_list = ["欢迎领导莅临指导！", "欢迎领导来视察工作！", "领导辛苦了！", "请领导多多提出宝贵的意见！"]
                        words_speak = random.choice(words_list)
                        tts_main(words_speak)
                        wav2pcm.audio_play(settings.SPEACK_FILE)
                    else:
                        tts_main("好的，再见，有什么事可以来找我哦！")
                        wav2pcm.audio_play(settings.SPEACK_FILE)
                        break
            except:
                tts_main("抱歉，我好像没有明白你说了什么")
                wav2pcm.audio_play(settings.SPEACK_FILE)
                continue


if __name__ == '__main__':
    start = XbtBot()
    start.run()


