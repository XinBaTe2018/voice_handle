# -*- coding: utf-8 -*-
'''
@auther: Liruijuan
@summary: 进行音频检测，当音量超过设定的阈值则开始录音，并将录音的结果存储到wav文件中
'''

import pyaudio
import wave
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 1


class Monitor():
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.count = 0

    def start(self):
        self.stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("开始缓存录音")


    def monitor(self):
        while True:
            self.start()
            self.count += 1
            print("开始第" + str(self.count) + "次检测")  # 设置循环20次时，停止运行程序
            for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
                data = self.stream.read(CHUNK)
                self.frames.append(data)
            audio_data = np.fromstring(data, dtype=np.short)
            large_sample_count = np.sum( audio_data > 800 )
            temp = np.max(audio_data)   # 使用最大因音量来控制
            if temp > 800:
                print('当前阈值：', temp)
                return True
            else:
                self.frames = []


    def record(self):
        # res = self.monitor()
        # if res:
            print("检测到信号,开始录音")
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS * 6)):
                data = self.stream.read(CHUNK)
                self.frames.append(data)
            print("录音结束")
            self.stop()

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        # p.terminate()     #注释掉，使循环继续

    # def __del__(self):
    #     self.p.terminate()

    def write_audio_to_wave(self, file_name):
        """ Write saved audio byte data to a file

        recordLen: length in seconds to record
        outWaveFile: filename to write wave file to

        """
        waveFile = wave.open(file_name, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(self.p.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()


if __name__ == '__main__':
    monitor = Monitor()
    monitor.record()
    monitor.write_audio_to_wave('vad_test.wav')

