#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import sqlite3
import json
import os
from define import *

def query_data(name_keyword, url_keyword):
    db_path = os.path.join(kBookmarkPath, kDataBaseName)
    db_path = os.path.expanduser(db_path)
    db = sqlite3.connect(db_path)

    query_data_sql = f"SELECT * FROM bookmark WHERE name LIKE '%{name_keyword}%' OR url LIKE '%{url_keyword}%' OR path LIKE '%{name_keyword}%' OR pinyin LIKE '%{name_keyword}%' order by adddate desc"
    # 如果是以#开头，则只查询path
    if name_keyword.startswith("#"):
        name_keyword = name_keyword[1:]
        # 使用空格分隔
        keywords = name_keyword.split(" ")
        if len(keywords) > 1 and len(keywords[1]) > 0:
            path = keywords[0]
            keword = keywords[1]
            # 查询path下name为keyword或url为keyword的数据
            query_data_sql = f"SELECT * FROM bookmark WHERE (path LIKE '%{path}%' OR pathpinyin LIKE '%{path}%') AND (name LIKE '%{keword}%' OR url LIKE '%{keword}%' OR pinyin LIKE '%{keword}%') order by adddate desc"
        else:
            query_data_sql = f"SELECT * FROM bookmark WHERE path LIKE '%{name_keyword}%' OR pathpinyin LIKE '%{name_keyword}%' order by adddate desc"
    rows = db.execute(query_data_sql).fetchall()
    db.close()
    return rows

def getAlfredItems(keywork):
    result = query_data(keywork, keywork)
    # 构建Alfred结果列表
    alfred_items = []
    for row in result:
        title, path, url, adddate, pinyin, pathpinyin = row
        title = f'[{path}]{title}'
        subtitle = f'[收藏时间:{adddate}]{url}'
        alfred_item = {
            'title': title,
            'subtitle': subtitle,
            'arg': url
        }
        alfred_items.append(alfred_item)

    print(json.dumps({'items': alfred_items}))


if __name__ == '__main__':
    arguments = sys.argv
    operation = arguments[1] if len(arguments) > 1 else None
    if operation:
        getAlfredItems(operation)
