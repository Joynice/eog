from pymongo import MongoClient
import base64
import time

uri = 'mongodb://admin:admin@192.168.0.119:27017/DropsDB?authSource=admin&authMechanism=SARAM-SHA-1'
conn = MongoClient(uri)

db = conn['DropsDB']
result = db['Result']
rules = db['rules']
keyword = db['keyword']
sec_event = db['sec_event']


# print(db)


def insert_rules(data):
    try:
        rules.insert(data)
        return True
    except Exception as e:
        print(e)
        return False


def find_rules():
    try:
        return rules.find()
    except Exception as e:
        return False


def find_one_rules(rule):
    try:
        return rules.find_one({"rule": rule})
    except Exception as e:
        return False


def delete_rule(rule):
    try:
        return (rules.delete_one({"rule": rule})).deleted_count
    except Exception as e:
        return False


def count_rule():
    try:
        return rules.count()
    except:
        return 0


class SecEvent(object):
    def __init__(self):
        self.sec_event = sec_event

    def find_event(self):
        return self.sec_event.find()

    def find_event_one(self, id):
        return self.sec_event.find_one({"_id": id})

    def decodeImage(self, img_data):
        if type(img_data) is str:
            self.new_img_data = bytes(img_data.get("img")[2:-1], encoding='utf8')
        img_code = base64.b64decode(self.new_img_data)
        with open('./{}.jpg'.format(str(time.time())), 'wb') as g:
            g.write(img_code)


s = SecEvent()
# print(s.find_event())
# for i in s.find_event():
#     print(i.get('_id'))
#     if i.get("img") == 'None':
#         pass
#     else:
#         decodeImage(i.get('img'))
