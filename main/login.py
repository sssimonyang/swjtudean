#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
@author: SSSimon Yang
@contact: yangjingkang@126.com
@file: login.py
@time: 2019/8/24 21:30
@desc: pip install baidu-aip
"""

import json
import os
from io import BytesIO

import requests
from PIL import Image

import config


def image_to_string(path):
    from aip import AipOcr
    APP_ID = config.API_ID  # 填你自己的ID
    API_KEY = config.API_KEY  # 填你自己的APIKEY
    SECRET_KEY = config.SECRET_KEY  # 填你自己的SECRETKEY
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    image = get_file_content(path)
    client.basicAccurate(image)
    options = {"language_type": "ENG"}
    result = client.basicAccurate(image, options)['words_result']
    if result:
        return result[0]['words'].strip()
    else:
        return


def login(user_id, user_password):
    s = requests.session()
    s.get("http://jwc.swjtu.edu.cn/service/login.html")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'jwc.swjtu.edu.cn',
        'Origin': 'http://jwc.swjtu.edu.cn',
        'Referer': 'http://jwc.swjtu.edu.cn/service/login.html',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        "username": user_id,
        "password": user_password,
        "url": "http://jwc.swjtu.edu.cn/index.html",
        "returnUrl": "",
        "area": ""
    }
    while True:
        response = s.get("http://jwc.swjtu.edu.cn/vatuu/GetRandomNumberToJPEG?test=1564814816379")
        image = Image.open(BytesIO(response.content))
        image.save('temp.png')
        random_string = image_to_string('temp.png')
        os.remove("temp.png")
        if random_string:
            data['ranstring'] = random_string
        else:
            continue
        response = s.post("http://jwc.swjtu.edu.cn/vatuu/UserLoginAction", data=data, headers=headers)
        if "验证码输入不正确" in response.text:
            continue
        if "用户不存在" in response.text:
            print("登录，用户名错误")
            raise Exception("用户名错误。")
        if "登录失败，密码输入不正确" in response.text:
            print("密码错误")
            raise Exception("密码错误。")
        if "登录成功" in response.text:
            print("Success")
            data = {
                "url": "http://dean.vatuu.com/vatuu/UserLoadingAction",
                "returnUrl": "",
                "loginMsg": json.loads(response.text)["loginMsg"]
            }
            s.post("http://dean.vatuu.com/vatuu/UserLoadingAction", data=data, headers=headers)
            return s


if __name__ == "__main__":
    s = login(user_id=config.user_id, user_password=config.user_password)
    print(s.cookies.get_dict())
