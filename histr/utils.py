# -*- codeing = utf-8 -*-
# @Time : 2021/12/1 下午10:00
# @Author : Histranger
# @File : utils.py
# @Software: PyCharm
import datetime
import json
import os
from pathlib import Path

import requests

# MD, import must add package name, otherwise `Error: While importing 'histr', an ImportError was raised.`
from histr.settings import StaticConfig

# The following two lines are just for test.
# import dotenv
# dotenv.load_dotenv('../.env')


class GetDataFromHiBlogAnswer(object):
    username = os.getenv('HIBLOG_USER', "YOU GUESS.")
    password = os.getenv('HIBLOG_PASSWORD', "YOU GUESS.")
    tmp_data_dir = os.path.join(StaticConfig.histr_PATH, 'tmp_data')
    token_path = os.path.join(tmp_data_dir, 'access_token.json')

    answer_random_item_API = "http://{}/answer/api/v1/oauth/answer_random_item".format(StaticConfig.IP)
    answer_token_API = "http://{}/answer/api/v1/oauth/token".format(StaticConfig.IP)

    def get_token(self):
        print(self.username, self.password)
        payload = {'username': self.username, 'password': self.password, 'grant_type': 'password'}
        res = requests.post(self.answer_token_API, data=payload)
        res = dict(res.json())
        access_token = None
        if res.get('token_type') == "Bearer":
            access_token = res.get('access_token')

        return access_token

    def write2json(self, access_token):
        # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
        Path(self.tmp_data_dir).mkdir(parents=True, exist_ok=True)
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
            print(access_token)
            self.write2json(access_token=access_token)

        headers = {"Authorization": f"Bearer {access_token}"}
        res = requests.get(self.answer_random_item_API, headers=headers)
        # print(json.dumps(res.json(), ensure_ascii=False))
        res = res.json()
        print(res)
        if res.get('code') == 404:
            return res.get("message")
        else:
            return res.get("content")


if __name__ == "__main__":
    token = GetDataFromHiBlogAnswer()
    ret = token.get_answer_random_item()
    print(ret)
