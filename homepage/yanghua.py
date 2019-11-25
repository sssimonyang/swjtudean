#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
@author: SSSimon Yang
@contact: yangjingkang@126.com
@file: yanghua.py
@time: 2019/8/25 11:30
@desc: conda install lxml psycopg2
"""
import datetime
import re
from urllib.parse import urljoin

import psycopg2
import requests
from lxml import etree

import config


def main():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"{date} 运行")
    c = conn.cursor()
    c.execute("SELECT name FROM yanghua")
    names = set([i[0] for i in c.fetchall()])

    s = requests.session()
    html = "http://xg.swjtu.edu.cn/web/Publicity/List"
    try:
        res = [s.get(html, timeout=3)]
    except ConnectionError:
        return

    pages = [etree.HTML(i.text) for i in res]
    lists = []
    results = []
    lists.extend(pages[0].xpath("//ul[@class='block-ctxlist Publicity']/li/h4"))
    for i in lists:
        temp = i.xpath("span")
        name = temp[0].xpath("a/text()")[0].strip()
        if "公示中" in temp[1].text and (name not in names):
            href = temp[0].xpath("a/@href")[0]
            href = urljoin(html, href)
            print(href)
            res = s.get(href, timeout=3)
            if "请先登录" in res.text:
                continue
            page = etree.HTML(res.text)
            div = page.xpath("//div[@class='right-content-side']")[0]
            a_list = div.xpath("//p[@class='pdf-down']/a")
            if a_list:
                for a in a_list:
                    file, filename = re.findall(r',[\'\"](.*)[\'\"],[\'\"](.*)[\'\"],[\'\"].*[\'\"]', a.get("href"))[0]
                    file_url = 'http://xgservice.swjtu.edu.cn/service/uploadserver/down/getfile?file=' + file + '|' + filename
                    with open(f"htmls/excel/{filename}", 'wb') as f:
                        f.write(requests.get(file_url).content)
                    a.attrib['href'] = file_url
            text = etree.tostring(div, encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
            results.append((name, text))
        else:
            break
    for i in results:
        name, text = i
        text = re.sub(r"'", "\"", text)
        c.execute(f"INSERT INTO yanghua (name,content,date) VALUES ('{name}','{text}','{date}')")
        print(f"{date} {name} 已插入")
    conn.commit()
    conn.close()


def to_file():
    c = conn.cursor()
    c.execute("SELECT id, name, content, date FROM yanghua")
    results = c.fetchall()
    for i in results:
        _, name, content, date = i
        with open(f"htmls/yanghua/{date}-{name}.html", 'w', encoding="utf-8") as f:
            f.write(content)


if __name__ == '__main__':
    conn = psycopg2.connect(dbname=config.dbname, user=config.user, password=config.password, host=config.host,
                            port=config.port)
    main()
    # to_file()
    conn.close()
