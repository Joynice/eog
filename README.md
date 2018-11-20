# eog
专家值守平台

## 日志功能模块开发

**添加功能日志记录**

**需求**：为实现对安全专家的行为约束。对审核的内容负责，审核态度认真仔细。能够记录审核专家的关键操作，特别是关系到数据库的增删改查操作。
如：专家审核某个单位的审核状态等。

**实现方法**：通过监控路由请求记录下请求的地址与参数或数据。
```angular2html
    path = request.path
    ip = request.remote_addr
```
并且不能对每个路由都监控，配置忽略监控路由的列表，对于被监控的路由产生的事件用字典的形式进行添加中文描述，方便前端用户查看。
日志的产生字段有专家姓名、专家职位（"安全专家"）、访问时间、访问ip、具体操作。
```angular2html
ignore_path=['/eog/events/','/eog/rules/','/eog/log/','/eog/resetpwd/','/eog/profile/','/eog/my_log/','/eog/','/eog/danger_event/','/eog/review_event/'
             ,'/eog/my_score/','/eog/my_review/','/eog/logout/'] # 不想被写进日志忽略的路由
path_and_operation_detail={'/eog/event_detail/':'查看安全事件{}详情'.format(request.form.get('event_id')),
                           '/eog/event_suggestion/':'审核{id}事件为{status}'.format(id=request.form.get('id'),status=request.form.get('status'))
                           } # 自定义添加被监测的日志详情说明
```

**数据库字段**

```angular2html
class Operate_Log(db.Document):
    meta = {'collection': 'operate_log'}
    realname = db.StringField()
    operate_time =db.DateTimeField(default=datetime.now)
    ip = db.StringField()
    path = db.StringField()
    operation = db.StringField()

```
**TODO(李然)**:增加日期的选择功能,能够选择点击某一段日期段，筛选某个时间段的记录

```angular2html
在数据库的分页查询的基础上。增加数据库选择时间段的查询。

注意：用`mongoengine`的分页查询和按照时间的倒序查询时，当查询的数据比较多的时候，会产生数据库缓存不足的错误
```
**登录**

目的：实现专家登录功能，限制未登录用户访问后台路由。

数据库字段

```angular2html
class User(db.Document):
    '''
    用户登录：用户名、密码、邮箱、真实姓名、加入时间、头像地址
    '''
    meta = {'collection': 'user'}
    _id = db.StringField(default=shortuuid.uuid)
    username = db.StringField(required=True, max_length=50)
    password = db.StringField(required=True, max_length=200)
    email = db.EmailField(required=True, max_length=100)
    realname = db.StringField(required=True, max_length=10)
    join_time = db.DateTimeField(required=False, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    avatar_path = db.StringField(required=False)

    def avatar(self):
        print(sep + 'static' + sep + 'eog' + sep + 'img' + sep + 'default' + sep + random.choice(
            os.listdir('./static/eog/img/default/')))
        return sep + 'static' + sep + 'eog' + sep + 'img' + sep + 'default' + sep + random.choice(
            os.listdir('./static/eog/img/default/'))
```
TODO:没有解决mongodb密码加密功能。

****




