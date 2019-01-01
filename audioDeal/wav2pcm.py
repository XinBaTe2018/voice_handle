# -*- coding: utf-8 -*-
'''
@auther: Liruijuan
@summary: 音频格式转化（wav -> pcm）；播放音频
'''
import os
from setting import settings
import pyaudio
import wave

CHUNK = 1024
p = pyaudio.PyAudio()

def wav_to_pcm(wav_file):
    # 假设wav_file = "音频文件.wav"
    # wav_file.spilr(".")得到["音频文件","wav"]拿出第一个结果"音频文件"与".pcm"拼接，得到结果"音频文件.pcm"
    pcm_file = "%s.pcm" % (wav_file.split(".")[0])

    # 就是此前在cmd窗口中输入命令，这里面就是让Python帮我们在cmd中执行命令
    os.system("%s -loglevel quiet -y -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s" % (settings.TRANSVERTER, wav_file, pcm_file))
    return pcm_file

# 使用pyaudio读取语音合成得到的音频文件
def audio_play(filename):
    wf = wave.open(filename, 'rb')

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream
    while len(data) > 0:
        data = wf.readframes(CHUNK)
        stream.write(data)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    # p.terminate()     #注释掉，使循环继续

if __name__ == '__main__':
    # file = wav_to_pcm("test.wav")
    audio_play(settings.SPEACK_PATH)

