# -*- codeing = utf-8 -*-
# @Time : 2021/12/1 下午10:00
# @Author : Histranger
# @File : utils.py
# @Software: PyCharm
import datetime
import json
import os

import requests

from dotenv import load_dotenv
from settings import StaticConfig

load_dotenv(os.path.join(os.path.dirname(StaticConfig.histr_PATH), '.env'))


class GetDataFromHiBlogAnswer(object):
    username = os.getenv('HIBLOG_USER', "YOU GUESS.")
    password = os.getenv('HIBLOG_PASSWORD', "YOU GUESS.")
    tmp_data_dir = os.path.join(StaticConfig.histr_PATH, 'tmp_data')
    token_path = os.path.join(tmp_data_dir, 'access_token.json')

    def get_token(self):
        payload = {'username': self.username, 'password': self.password, 'grant_type': 'password'}
        res = requests.post('http://121.40.58.243/answer/api/v1/oauth/token', data=payload)
        res = dict(res.json())
        access_token = None
        if res.get('token_type') == "Bearer":
            access_token = res.get('access_token')

        return access_token

    def write2json(self, access_token):
        dic = {
            "timestamp": datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S'),
            "access_token": access_token,
        }
        with open(self.token_path, 'w', encoding='utf-8') as f:
            json.dump(dic, f)

    def get_answer_random_item(self) -> str:
        """return string"""
        access_token = None
        if os.path.exists(self.token_path) and os.path.isfile(self.token_path):
            with open(self.token_path, 'r', encoding='utf-8') as f:
                token_dict = json.load(f)
            if token_dict and token_dict.get('timestamp'):
                timestamp = datetime.datetime.strptime(token_dict.get('timestamp'), '%Y/%m/%d-%H:%M:%S')
                if timestamp + datetime.timedelta(minutes=55) > datetime.datetime.now():
                    access_token = token_dict.get('access_token')
        if access_token is None:
            access_token = self.get_token()
            self.write2json(access_token=access_token)

        headers = {"Authorization": f"Bearer {access_token}"}
        res = requests.get(f'http://192.168.3.127:5001/answer/api/v1/oauth/answer_random_item',
                           headers=headers)
        res = res.json()
        # print(json.dumps(res.json(), ensure_ascii=False))
        if res.get('code') == 404:
            return res.get("message")
        else:
            return res.get("content")


if __name__ == "__main__":
    token = GetDataFromHiBlogAnswer()
    ret = token.get_answer_random_item()
    print(ret)
