#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: SSSimon Yang
@contact: yangjingkang@126.com
@file: chrome.py
@time: 2019/4/14 23:10
@desc: pip install baidu-aip
"""
from selenium import webdriver

import config
from main.login import login


def main():
    s = login(config.user_id, config.user_password)
    cookies = s.cookies.get_dict()
    driver = webdriver.Chrome()
    driver.get("http://jwc.swjtu.edu.cn/vatuu/UserFramework")
    for i in cookies:
        driver.add_cookie({"name": i, "value": cookies[i]})
    driver.get("http://jwc.swjtu.edu.cn/vatuu/UserFramework")


if __name__ == '__main__':
    main()
