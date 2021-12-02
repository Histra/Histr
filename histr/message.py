# -*- codeing = utf-8 -*-
# @Time : 2021/12/2 下午1:17
# @Author : Histranger
# @File : message.py
# @Software: PyCharm
import time


class Message(object):
    message_type = 'unkown'


class TextMessage(Message):
    message_type = 'text'

    xml_format = \
        '''
        <xml>
         <ToUserName><![CDATA[{fan_id}]]></ToUserName>
         <FromUserName><![CDATA[{histr_id}]]></FromUserName>
         <CreateTime>{time_int}</CreateTime>
         <MsgType><![CDATA[{message_type}]]></MsgType>
         <Content><![CDATA[{message_content}]]></Content>
        </xml>
        '''

    def __init__(self, from_user_name, to_user_name, message):
        self.from_user_name = from_user_name
        self.to_user_name = to_user_name
        self.xml_message = self.xml_format.format(
            fan_id=to_user_name,
            histr_id=from_user_name,
            time_int=int(time.time()),
            message_type=self.message_type,
            message_content=message
        )
