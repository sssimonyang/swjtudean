#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
@author: SSSimon Yang
@contact: yangjingkang@126.com
@file: evaluation.py
@time: 2019/9/9 20:39
@desc: you may run across connect error, if such error occurs, just rerun the code
"""
import csv
import re
import time
from datetime import datetime
from random import random
from urllib import parse

from lxml import etree
from urllib3 import HTTPSConnectionPool

import config
from mail import send_mail
from main.login import login


def access(s):
    s.get("http://jwc.swjtu.edu.cn/vatuu/AssessAction?setAction=index")
    response = s.get("http://jwc.swjtu.edu.cn/vatuu/AssessAction?setAction=list")
    questionnaires = re.findall(r"<a href=\"(.*?)\">填写问卷</a>", response.text)
    n = len(questionnaires)

    for url in questionnaires:
        url = parse.urljoin("http://jwc.swjtu.edu.cn/", url)
        if single_access(s, url):
            n = n - 1
    return f"有 {len(questionnaires)} 门课程需要评价，已完成 {len(questionnaires) - n} 门课的评价，谢谢使用。"


def evaluate(s):
    response = s.get("http://jwc.swjtu.edu.cn/vatuu/StudentScoreInfoAction?setAction=studentMarkUseProgram")
    if "你还没有完成评价" in response.text:
        return access(s)
    else:
        return "您没有课程需要评价。"


def single_access(s, url):
    lid = parse.parse_qs(parse.urlparse(url).query)['lid'][0]
    response = s.get(url)
    time.sleep(15)  # 最短时间15s
    page = etree.HTML(response.text)
    problems = page.xpath("//form[@name='answerForm']/div[@class='answerDiv questionDiv']/div[1]/input/@name")
    problems.extend(
        page.xpath("//form[@name='answerForm']/div[@class='post-problem questionDiv']/div/textarea/@name"))
    ids = [problem.replace("problem", '') for problem in problems]
    values = page.xpath("//form/div[@class='answerDiv questionDiv']/div[1]/input/@value")
    id = "_" + ("_".join(ids))
    answer = "_" + ("_".join(values + ["都很好", "都很好"]))
    assess_id = page.xpath("//form[@name='answerForm']/input/@value")[0]
    data = {
        "id": id,
        "answer": answer,
        "scores": "_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0__",
        "percents": "_10.0_10.0_10.0_10.0_10.0_10.0_10.0_10.0_10.0_10.0_0.0_0.0_0.0_0.0_0.0_0.0_0.0_0.0",
        "assess_id": assess_id,
        'templateFlag': '0',
        't': str(random()),
        'keyword': "null",
        'setAction': 'answerStudent',
        "teacherId": None,
        'logId': lid
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Host': 'jwc.swjtu.edu.cn',
        'Origin': 'http://jwc.swjtu.edu.cn',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': url,
        'Upgrade-Insecure-Requests': '1',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    response = s.post("http://jwc.swjtu.edu.cn/vatuu/AssessAction", data=data, headers=headers)
    if "操作成功" in response.text:
        return True
    else:
        return False


def main(csv_file):
    """
    process csv to run many ids in line
    you can change some code to use your own file
    :param csv_file: csv filepath
    :return:
    """
    with open(csv_file, encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        rows = list(csv_reader)[6:]
    today = datetime.now().date()
    results = []
    for row in rows:
        over_time = datetime.strptime(row[2], '%d-%b-%Y %H:%M:%S')
        if over_time.date() == today:
            user_id = row[5].strip()
            user_password = row[6]
            email = row[-2].strip()
            results.append(process(user_id, user_password, email))
    print("/n".join(results))


def process(user_id, user_password, email=''):
    """
    do a single evaluation task
    :param user_id: your user_id like '201*****48'
    :param user_password: your user_password I don't recommend user space in password
    :param email: email address to send the info of your task
    :return:
    """
    try:
        s = login(user_id, user_password)
    except HTTPSConnectionPool:
        print(f"{user_id} Error")
        return f"{user_id} failed"
    except Exception as e:
        message = str(e)
    else:
        message = evaluate(s)
    print(f"{user_id} 自动评价结果，{message}")
    print("---------------------------")
    if email:
        send_mail(send_tos=[email], name="SSSimon Yang", subject=f"{user_id} 自动评价结果",
                  text=message)
    return f"{user_id} success"


if __name__ == '__main__':
    # main(r'************.csv') 
    process(config.user_id, config.user_password)
    # process(config.user_id, config.user_password, config.user_email)
