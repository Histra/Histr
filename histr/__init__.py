# -*- codeing = utf-8 -*-
# @Time : 2021/12/1 下午6:08
# @Author : Histranger
# @File : __init__.py.py
# @Software: PyCharm
import logging
import os.path
from logging.handlers import RotatingFileHandler

from flask import Flask

from histr.blueprints.token import bp_token
from histr.settings import StaticConfig

from dotenv import load_dotenv

load_dotenv('.env')

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app():
    app = Flask('histr')

    register_blueprints(app)
    register_logging(app)

    return app


def register_blueprints(app):
    app.register_blueprint(bp_token, url_prefix="/histr/token")


def register_logging(app):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    os.makedirs(basedir, exist_ok=True)
    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/histr.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug and not app.logger.handlers:
        app.logger.addHandler(file_handler)
