# -*- coding: utf-8 -*-
'''
@auther: Liruijuan & Liyaguo
@summary: 运行的主程序，主要实现检测录音 + 语音识别 + 核心机器人回答 + 语音合成
'''
from core import wav2pcm
import os, time
from core.MyRobert import bot, MyThread
from core.TuLinRobert import TuLin
from core.speakout import tts_main
from setting import settings
from core.sound2wordXF import wordfromS     # 该文档使用讯飞api进行语音识别
from core.sound2wordBD import asr_main      # 此处使用百度api进行语音识别
import core.moni_record
import core.vad_speakout
from core.synonyms import sy
import re
import random
import multiprocessing

def rebot_respond(words):
    t = MyThread(TuLin, args=(words,))
    t.setDaemon(True)
    t.start()
    t1 = MyThread(sy, args=(words,))
    t1.setDaemon(True)
    t1.start()
    chatterbot_respone = bot.get_response(words)

    if chatterbot_respone != "Tulin reply":
        print("first")
        response = chatterbot_respone
    else:
        t1.join()
        response = t1.get_result()
        if response == None:
            print('tulin')
            t.join()
            response = t.get_result()
    return response

def tts_qps(respond_words):
    # respond_words = '这几天心里颇不宁静。今晚在院子里坐着乘凉，忽然想起日日走过的荷塘，在这满月的光里，总该另有一番样子吧。月亮渐渐地升高了，墙外马路上孩子们的欢笑，已经听不见了；'
    result_list = core.vad_speakout.text_vad(respond_words)

    make_wave = multiprocessing.Process(target=core.vad_speakout.make_data, args=(core.vad_speakout.queue, result_list,))  # 生成数据进程
    read_wave = multiprocessing.Process(target=core.vad_speakout.handle_data, args=(core.vad_speakout.queue,core.vad_speakout.lock))
    read_wave.daemon = True  # 设为守护线程

    make_wave.start()
    read_wave.start()

    make_wave.join()
    # read_wave.join()
    print('Ended!')

def vad_read(filedir):
    filename = os.listdir(filedir)  # 得到文件夹下的所有文件名称
    i = 0
    while i < len(filename):
        (file_n, extension) = os.path.splitext(filename[i])
        # print(extension)
        if extension == '.wav':
            file_name = os.path.join(filedir, filename[i])
            i += 1
            wav2pcm.audio_play(file_name)


if __name__ == '__main__':
    while True:
        try:
            core.moni_record.monitor(settings.LISTEN_FILE)
            start = time.time()
            words = wordfromS(settings.LISTEN_FILE)  # 读取录音文件，通过讯飞API实现语音转写
            stop1 = time.time()
            # print("讯飞API:%s" % (stop1 - start))

            results = re.findall(r'(再见|goodbye|byebye|退出|再会|待会见|张总|陈总|李总|王总|赵总|刘总)', words)
            # print(results)
            if len(results) == 0:
                if words is not None:
                    response = rebot_respond(words)
                    stop2 = time.time()
                    print("思考时间:%s" % (stop2 - stop1))

                    tts_qps(str(response))
                    stop3 = time.time()
                    print("语音合成时间%s" % (stop3 - stop2))
                    print(stop3 - start)
                    #os.system("%s  %s" % (settings.PLAY_MEDIA, settings.SPEACK_FILE))

                else:
                    tts_main("不好意思，您可以再说一遍吗？",settings.SPEACK_FILE)
                    wav2pcm.audio_play(settings.SPEACK_FILE)

            elif [x for x in results if x in ["张总","陈总","王总","李总","赵总","刘总"]] :
                words_list = ["欢迎领导莅临指导！","欢迎领导来视察工作！","领导辛苦了！","请领导多多提出宝贵的意见！"]
                words_speak = random.choice(words_list)
                tts_main(words_speak,settings.SPEACK_FILE)
                wav2pcm.audio_play(settings.SPEACK_FILE)

            else:
                tts_main("好的，再见，有什么事可以来找我哦！",settings.SPEACK_FILE)
                wav2pcm.audio_play(settings.SPEACK_FILE)
                break

        except:
            tts_main("抱歉，我好像没有明白你说了什么",settings.SPEACK_FILE)
            wav2pcm.audio_play(settings.SPEACK_FILE)
            continue
