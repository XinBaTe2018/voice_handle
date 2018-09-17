import re
import json
from concurrent.futures import  ThreadPoolExecutor
list3 =[]
with open("new_synomys.txt","r",encoding='utf-8') as f:
   with open('new_synomys.json','w',encoding='utf-8') as h:
    for line in f:
            list1,list2 = line.strip().split("\t")
            if len(list1)>1 and len(list2) >1:
                list3.append([list1,list2])
    h.write(json.dumps(list3))

# def load_data():
#     with open("new_synomys.json", 'r') as load_f:
#         for line in json.load(load_f):
#             sign= yield line
#             if sign == 'stop':
#                 break
#
# def task():
#     load_data1 = load_data()
#     for k in load_data1:
#         try:
#             print(k)
#             if k == ['匹夫', '个人']:
#                 load_data1.send('stop')
#         except:
#             break

# if __name__ == '__main__':
#     # pool = ThreadPoolExecutor(20)
#     for i in range(3):
#         task()
    # pool.shutdown()  # join结束

# try:
#     print(next(load_data))
#     print(next(load_data))
#     load_data.send('stop')
# except StopIteration:
#     print(12)

# next(load_data)

# d= {1:[23,45]}
# print(type(d.values()))
# l = [1,2,3]
# l[1]=3
# print([])
# h=['今日', '是', '儿童节']
# print("".join(h))

# h=set(['今日', '是', '儿童节'])
# h.add('儿童节')
# print(h)
# import random
# h=[]
# rd = random.choice(list(h))
# print(rd)