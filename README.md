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


实现方法：获得表单的数据、通过Post方式提交到后端，进行后端进行表单验证，如果同user库邮箱、密码相匹配则重定向到后台首页，反之提示用户账号或者密码错误。详细实现过程可以看下源码，如有疑问，不吝赐教。


表单验证字段

````angular2html
class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()
````

TODO:没有解决mongodb密码加密功能。

**注册**


目的：实现用户根据自己的邮箱实现注册功能。

实现方法：前端通过Js获得用户填写的表单数据，前端进行些简单的验证如：邮箱格式、两次输入密码是否相同、以及在60s内无法再次点击发送邮件的限制，可以减轻服务器压力，防止恶作剧。将获得的表单数据通过Ajax Post方法发送给后端，后端进行表单验证，如果表单验证通过，就参入user库，否则给前端返回相应错误。

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

表单验证字段
````angular2html
class SignupForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱地址！'),InputRequired(message='请输入邮箱地址')])
    email_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式的邮箱验证码！'), InputRequired(message='请输入邮箱验证码')])
    username = StringField(validators=[Length(2, 20, message='请输入正确格式的用户名'), InputRequired(message='请输入用户名')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\./]{6,20}', message='请输入正确格式的密码'), InputRequired(message='请输入密码')])
    password2 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\./]{6,20}', message='请输入正确格式的密码'), InputRequired(message='请再次输入密码')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式的图形验证码！'), InputRequired(message='请输入图形验证码')])
    realname = StringField(validators=[InputRequired(message='请输入真实姓名'), InputRequired(message='请输入真实姓名')])

    def validate_email_captcha(self, field):
        captcha = field.data
        email = self.email.data
        try:
            captcha_cache = zlcache.get(email)
        except:
            raise ValidationError(message='邮箱验证码不存在！')
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError(message='邮箱验证码错误！')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        try:
            graph_captcha_mem = zlcache.get(graph_captcha.lower())
        except:
            raise ValidationError(message='图形验证码不存在！')
        print(graph_captcha_mem, graph_captcha)
        if not graph_captcha_mem:
            raise ValidationError(message='图形验证码错误！')
````


**重置密码**

目的：让忘记密码的用户重置密码。

实现方法：用户输入需要重置密码邮箱、通过发送邮箱验证码来进行



