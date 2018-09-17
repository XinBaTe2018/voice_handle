from chatterbot.trainers import ChatterBotCorpusTrainer
import os,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
corpus_file = os.path.join(BASE_DIR,"database/jsonfile/test.json")
from core.MyRobert import bot
bot.set_trainer(ChatterBotCorpusTrainer)

# 使用中文语料库训练它
if __name__ == '__main__':
    bot.train(corpus_file)