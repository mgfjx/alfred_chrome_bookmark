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

    query_data_sql = f"SELECT * FROM bookmark WHERE name LIKE '%{name_keyword}%' OR url LIKE '%{url_keyword}%' OR path LIKE '%{name_keyword}%' OR pinyin LIKE '%{name_keyword}%'"
    rows = db.execute(query_data_sql).fetchall()
    db.close()
    return rows

def getAlfredItems(keywork):
    result = query_data(keywork, keywork)
    # 构建Alfred结果列表
    alfred_items = []
    for row in result:
        title, path, url, adddate, pinyin = row
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
