class Config(object):
    SECRET_KEY = 'hard_word'
    EVENT_PER_PAGE = 15
    RULE_PER_PAGE = 7
    LOG_PER_PAGE = 19

    # REDIS 数据库配置
    REDIS_HOST = '10.63.3.62'  # yuqing
    # REDIS_HOST = '192.168.0.119'#drops
    REDIS_PORT = 6379
    REDIS_TASK_DB = 1
    REDIS_SOCKET_DB = 15
    REDIS_PASSWORD = ''
    REDIS_DECODE_RESPONSES = True
    REDIS_ENCODING = 'utf-8'


class DevelopmentConfig(Config):
    MONGODB_SETTINGS = {'DB': "myDev",
                        "host": 'mongodb://10.63.3.62:27017/myDev'}  #yuqing
    # MONGODB_SETTINGS = {'DB': "myDev",
    #                     "host": 'mongodb://admin:admin@192.168.0.119:27017/myDev?authSource=admin&authMechanism=SCRAM-SHA-1'} #drops
    # 发送者邮箱的服务器地址
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    # MAIL_USE_SSL
    MAIL_USERNAME = '1125365907@qq.com'
    MAIL_PASSWORD = 'fymamdgjrovehgcd'
    MAIL_DEFAULT_SENDER = '1125365907@qq.com'

    CMS_USER_ID = 'DSADSAD1551512'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prodection': ProductionConfig,
    'default': DevelopmentConfig
}
