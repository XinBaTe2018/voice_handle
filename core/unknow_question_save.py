# -*- coding: utf-8 -*-
'''
@auther: Li Yaguo
@summary: 储存机器人没能回答的问题
'''
from setting import settings
import datetime
from pymongo import MongoClient
class Singletion:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,"_instance"):
            cls._instance = super(Singletion,cls).__new__(cls)
        return cls._instance



class UnQuetion(Singletion):
    def __init__(self,ip,port,db,table):
        self.ip = ip
        self.port = port
        self.time=self.gettime()
        self.conn(db,table)


    def conn(self,db,table):
        client = MongoClient(self.ip, self.port)
        db = client[db]
        self.collection = db[table]

    def dump(self,words):
        self.collection.insert({'question':words,'time':self.time})

    @classmethod
    def conndb(cls):
        obj = cls(
            settings.IP,
            settings.PORT,
            settings.DB,
            settings.TABLE
        )
        return obj

    @staticmethod
    def gettime():
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        return time


if __name__ == '__main__':
    s=UnQuetion.conndb()
    s.dump("你好")
