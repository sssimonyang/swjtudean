#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
@author: SSSimon Yang
@contact: yangjingkang@126.com
@file: login.py
@time: 2019/11/27 17:01
@desc: curate function
"""

import argparse

import config
from personal_page.evaluation import process

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--id", help="specify your user id")
    parser.add_argument("-pw", "--password", help="specify your user password")
    args = parser.parse_args()
    if args.id and args.password:
        process(args.id, args.password)
    else:
        process(config.user_id, config.user_password)
