from pymongo import MongoClient
import re,os

BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file=os.path.join(BASE_DIR,"database/jsonfile/test.json")
client = MongoClient("localhost",27017)
db = client.xbt
collection = db.test

def load_json_file(file):
    list1 = []
    for item in collection.find({"category":re.compile("医学健康")}):
        list1.append([item.get("question"),item.get("answer")])
    data_dict = dict(conversations=list1)
    with open(file,'w') as f:
        import json
        f.write(json.dumps(data_dict))
if __name__ == '__main__':
    load_json_file(file)