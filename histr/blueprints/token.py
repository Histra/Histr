# -*- codeing = utf-8 -*-
# @Time : 2021/12/1 下午6:15
# @Author : Histranger
# @File : token.py
# @Software: PyCharm
import hashlib
import os

from flask import Blueprint, request, make_response, current_app

bp_token = Blueprint('token', __name__)


@bp_token.route("/")
def index():
    try:
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        token = os.getenv("PERSONAL_TOKEN", "you guess.")

        ttn_list = sorted([token, timestamp, nonce])

        sha1 = hashlib.sha1(''.join(ttn_list).encode('utf-8'))
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            response = make_response(echostr)
            current_app.logger.info("access token succeed.")
            return response
        else:
            current_app.logger.info("hashcode({}) != signature({})".format(hashcode, signature))
    except Exception as e:
        current_app.logger.info("{}".format(str(e)))

    return ""
