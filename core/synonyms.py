from core.MyRobert import bot
from synom.synonyms_replace import SynonymsReplacer
from setting.settings import *
from concurrent.futures import ThreadPoolExecutor
import random



class Synons:
    def __init__(self, words):
        self.result = set()
        self.words = words

    def replace(self):
        if len(self.words) >= 1:
            s = SynonymsReplacer(SYNO_FILES)
            result = s.get_syno_sents_list(self.words)
            return result
        else:
            print("没有声音")
    def chatbot_responae(self,response_obj):
        response = response_obj.result()
        if response != 'Tulin reply':
            self.result.add(response)
    def search(self):
        result = self.replace()
        print(result)
        if len(result) >1:
            pool = ThreadPoolExecutor(len(result) - 1)
            for word in result[1:]:
                pool.submit(bot.get_response, word).add_done_callback(self.chatbot_responae)
            pool.shutdown()
        else:
            print("没有声音1")


def sy(words):

    s= Synons(words)
    s.search()
    result = list(s.result)
    if result==[]:
        return None
    else:
        rd_result = random.choice(list(s.result))
        return rd_result


if __name__ == '__main__':
#     sy = Synons("今天儿童节")
#     sy.search()
#     if list(sy.result)==[]:
#         print(122)
    list1 =["吸烟的危害是什么","环境和健康有什么联系？"]
    for i in list1:
        sy = Synons(i)
        sy.search()
    print(sy.result)