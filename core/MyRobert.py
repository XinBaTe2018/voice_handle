from chatterbot import ChatBot
import threading
from setting import settings

bot = ChatBot("Terminal",
              storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
              logic_adapters=[
                  {'import_path': "chatterbot.logic.BestMatch"},
                  {
                      'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                      'threshold': settings.THRESHOLD,
                      'default_response': "Tulin reply"
                  },
              ],
              filters=[
                  'chatterbot.filters.RepetitiveResponseFilter'
              ],

              input_adapter="chatterbot.input.VariableInputTypeAdapter",
              output_adapter="chatterbot.output.OutputAdapter",
              database_uri="mongodb://localhost:27017/",
              database="xbt",
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
