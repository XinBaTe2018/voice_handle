from pymongo import MongoClient
import re,os
from core.MyRobert import bot
client = MongoClient("localhost",27017)
db = client.xbt
collection = db.test
'''
如果一个已经训练好的chatbot，你想取出它的语料，用于别的chatbot构建，可以这么做
'''

# 把语料导出到json文件中
bot.trainer.export_for_training('./my_export.json')