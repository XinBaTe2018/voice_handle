from core import wav2pcm
import os, time
from core.MyRobert import bot, MyThread
from core.TuLinRobert import TuLin
from core.speakout import tts_main
from setting import settings
from core.sound2wordXF import wordfromS     # 该文档使用讯飞api进行语音识别
import core.moni_record


if __name__ == '__main__':
    while True:
        try:
            core.moni_record.monitor(settings.LISTEN_FILE)
            start = time.time()
            words = wordfromS(settings.LISTEN_FILE)  # 读取录音文件，通过讯飞API实现语音转写
            stop1 = time.time()
            print("讯飞API:%s" % (stop1 - start))
            if str(words) not in ["再见，", "good bye，", "退出，"]:
                chatterbot_respone = bot.get_response(words)
                t = MyThread(TuLin, args=(words,))
                t.setDaemon(True)
                t.start()
                if chatterbot_respone != "Tulin reply":
                        response = chatterbot_respone
                else:
                    t.join()
                    response = t.get_result()
                stop2 = time.time()
                print("思考时间:%s" % (stop2 - stop1))
                tts_main(str(response))
                stop3 = time.time()
                print("语音合成时间%s" % (stop3 - stop2))
                print(stop3 - start)
                #os.system("%s  %s" % (settings.PLAY_MEDIA, settings.SPEACK_FILE))

                wav2pcm.audio_play(settings.SPEACK_FILE)
            else:
                tts_main("好的，再见，有什么事可以来找我哦！")
                wav2pcm.audio_play(settings.SPEACK_FILE)
                break

        except:
            tts_main("我好像没有明白你说了什么")
            wav2pcm.audio_play(settings.SPEACK_FILE)
            continue
