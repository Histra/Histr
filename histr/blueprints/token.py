# -*- codeing = utf-8 -*-
# @Time : 2021/12/1 下午6:15
# @Author : Histranger
# @File : token.py
# @Software: PyCharm
import hashlib
import os

import xmltodict
from flask import Blueprint, request, make_response, current_app, jsonify, redirect, url_for

from histr.message import TextMessage
from histr.utils import GetDataFromHiBlogAnswer

bp_token = Blueprint('token', __name__)


@bp_token.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return redirect(url_for('token.access_token'))
    else:
        return redirect(url_for('token.response'))


@bp_token.route("/response", methods=["POST"])
def response():
    # print(request.get_data().decode('utf-8'))
    xml_data = request.get_data().decode('utf-8').strip()
    dict_data = xmltodict.parse(xml_data)
    dict_data = dict_data["xml"]

    if dict_data["MsgType"] == "text":
        content = dict_data["Content"]
        from_user_name = dict_data["FromUserName"]
        to_user_name = dict_data["ToUserName"]
        answer = GetDataFromHiBlogAnswer().get_answer_random_item()
        xml_message = TextMessage(to_user_name, from_user_name, answer).xml_message
        xml_response = make_response(xml_message)
        xml_response.content_type = 'application/xml'
        return xml_response

    return "success"


@bp_token.route("/access_token")
def access_token():
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

    return jsonify({
        "Histranger": "终于被你发现我啦!"
    })
