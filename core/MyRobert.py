from chatterbot import ChatBot
import threading
from setting import settings

bot = ChatBot("Terminal",
              storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
              logic_adapters=[
                  {'import_path': "chatterbot.logic.BestMatch"}, # BestMatch 逻辑adater根据与输入语句最接近的匹配的已知响应返回响应
                  {
                      'import_path': 'chatterbot.logic.LowConfidenceAdapter',# LowConfidenceAdapter当高信度响应未知时，返回具有高置信度的默认响应。
                      'threshold': settings.THRESHOLD,
                      'defa'
                      'ult_response': "Tulin reply"
                  },
              ],
              filters=[
                  'chatterbot.filters.RepetitiveResponseFilter' #这是一个滤波器,它的作用是滤掉重复的回答
              ],

              input_adapter="chatterbot.input.VariableInputTypeAdapter",
              output_adapter="chatterbot.output.OutputAdapter",
              database_uri="mongodb://localhost:27017/",    # 设置你的数据库所在的地址端口号
              database="xbt",       #这是你的数据库名称,如果没有,首次他会自动创建
              read_only=True,
              )


class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None
