<<<<<<< HEAD
class Config(object):
    SECRET_KEY = 'hard_word'
    EVENT_PER_PAGE = 15
    RULE_PER_PAGE = 7


class DevelopmentConfig(Config):
    MONGODB_SETTINGS = {'DB': "myDev",
                        "host": 'mongodb://admin:admin@192.168.0.119:27017/myDev?authSource=admin&authMechanism=SCRAM-SHA-1'}
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
=======
class Config(object):
    SECRET_KEY = 'hard_word'
    EVENT_PER_PAGE = 15
    RULE_PER_PAGE = 7


class DevelopmentConfig(Config):
    MONGODB_SETTINGS = {'DB': "myDev",
                        "host": 'mongodb://admin:admin@192.168.0.119:27017/myDev?authSource=admin&authMechanism=SCRAM-SHA-1'}
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
>>>>>>> 6e9c628b092a4d60e546850fc6b0979f66f8ae3a
