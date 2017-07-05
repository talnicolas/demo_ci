# /instance/config.py

import os

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgres://ajbtuzbq:GBzd5nVae0xkzXa2tcFSB0mV6gIAuB-D@stampy.db.elephantsql.com:5432/ajbtuzbq'
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://ajbtuzbq:GBzd5nVae0xkzXa2tcFSB0mV6gIAuB-D@stampy.db.elephantsql.com:5432/ajbtuzbq'
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
