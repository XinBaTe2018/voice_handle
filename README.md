# Voice_handle
主要针对于汉语进行  
语音听写+会话机器人+语音合成
## 一、简介
*Voice-handle*是用Python所写，借助PyCharm进行编译。  
*Voice-handle*可以支持Python3.X
## 二、使用方式  
### 1. bin启动文件  
包含main主程序  
### 2. core核心代码文件  
moni_record: 检测信号并进行语音录制  
get_token: 获取百度API许可  
MyRobert: 自己的会话内核  
TuLingRobert: 图灵机器人会话  
sound2wordXF: 讯飞API语音听写  
sound2wordBD: 百度API语音识别  
speakout: 百度语音合成  
wav2pcm: 实现音频转换和音频播放  
***用到的工具：***  
1.录音过程——pyaudio  
2.播放过程——ffmpeg工具
### 3. corpus  
从数据库提取语料，转化为json文件格式  
### 4. database文件  
jsonfile 用于训练的预料  
listen 语音识别生成的文件  
speak 语音合成的文件  
### 5. setting  
配置文件  
### 6. training  
bulid_corpus 构建语料库文件  
summary 中心思想提取文件

## 三、Version
当前版本 : 0.0.0.1  