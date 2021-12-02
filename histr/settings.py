# -*- codeing = utf-8 -*-
# @Time : 2021/12/1 下午6:23
# @Author : Histranger
# @File : settings.py
# @Software: PyCharm
import os


MYSQL_USERNAME = os.getenv('MYSQL_HISTR_USERNAME', 'You guess.')
MYSQL_PASSWORD = os.getenv('MYSQL_HISTR_PASSWORD', 'You guess.')
MYSQL_HOST = os.getenv('MYSQL_HISTR_HOST', 'You guess.')
MYSQL_DATABASE_NAME = os.getenv('MYSQL_HISTR_DATABASE_NAME', 'You guess.')


class StaticConfig(object):
    histr_PATH = os.path.abspath(os.path.dirname(__file__))
    IP = "121.40.58.243"


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'histranger')


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'. \
        format(MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE_NAME)


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'. \
        format(MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE_NAME)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}