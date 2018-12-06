from datetime import datetime
from exts import db


class Event_Auto_Id(db.Document):
    '''
    ID自增参照对象，每次调用`auto_id`后，得到`sequence_value`的值。然后更新`sequence_value`的值+1。
    '''
    meta = {'collection': 'event_id'}
    _id = db.StringField(required=False, primary_key=True, default='auto_id')
    sequence_value = db.IntField(default=0)


class Rule(db.Document):
    '''
    规则数据库：包含规则、类型、等级、描述、建议、添加时间、命中次数
    '''
    meta = {'collection': 'rules'}
    # _id =db.StringField(primary_key=True)
    # id = db.StringField(required=False,primary_key=False)
    rule = db.StringField(required=False)
    type = db.StringField(required=False)
    leave = db.StringField(required=False)
    des = db.StringField(required=False)
    suggestion = db.StringField(required=False)
    create_time = db.DateTimeField(required=False, default=datetime.now)
    hit_count = db.IntField(default=0)


class Event_Spider(db.Document):
    '''
    爬虫匹配到的事件数据库：自增长ID、自定义ID、域名、任务ID、命中的规则、来源、首次发现时间、最新发现事件、
                            审核详情、审核状态、快照
    '''
    meta = {'collection': 'sec_event'}
    _id = db.IntField(required=False, primary_key=True)
    id = db.StringField(required=False)
    domain = db.StringField(required=False)
    jobid = db.StringField(required=False)
    event = db.ReferenceField(Rule)
    _from = db.StringField(required=False)
    first_time = db.DateTimeField(default=datetime.now)
    last_time = db.ListField(required=False)
    audit = db.ListField(required=False)
    status = db.StringField(required=False)
    img = db.StringField(required=False)


class Event_Search_Engine(db.Document):
    '''
    搜索引擎事件数据库：自增长ID、自定义ID、域名、任务ID、命中的规则、来源、首次发现时间、最新发现事件、
                        审核详情、审核状态、快照
    '''
    meta = {'collection': 'sec_event'}
    _id = db.IntField(required=False, default='num')
    id = db.StringField(required=False)
    domain = db.StringField(required=False)
    jobid = db.StringField(required=False)
    event = db.StringField(required=False)
    keyword = db.StringField(required=False)
    _from = db.StringField(required=False)
    first_time = db.DateTimeField(default=datetime.now)
    last_time = db.ListField(required=False)
    audit = db.ListField(required=False)
    status = db.StringField(required=False)
    suggestion = db.StringField(required=False)
    img = db.StringField(required=False)


class All_Result(db.Document):
    '''
    一次域名扫描后的结果：扫描时间、响应code、域名、任务id、事件列表
    '''
    meta = {'collection': 'all_result'}
    time = db.DateTimeField(default=datetime.now)
    code = db.IntField()
    domain = db.StringField()
    jobid = db.StringField()
    keyword_data = db.ListField()
    jump_url = db.ListField()
    events_list = db.ListField()
    websousec = db.StringField()
    img = db.StringField()
    message = db.StringField()


class Operate_Log(db.Document):
    meta = {'collection': 'operate_log'}
    realname = db.StringField()
    operate_time = db.DateTimeField(default=datetime.now)
    ip = db.StringField()
    path = db.StringField()
    operation = db.StringField()
    today = db.DateTimeField(requried=False)
