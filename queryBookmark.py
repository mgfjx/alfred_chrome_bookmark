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

    keywords = [k.strip() for k in name_keyword.split()] if name_keyword else []
    keywords = [k for k in keywords if k]  # 移除空字符串

    # 2. 构建 name_conditions（每个关键字在三个字段中匹配）
    name_conditions = []
    for k in keywords:
        # 转义单引号防止 SQL 注入（简易处理，建议使用参数化查询）
        safe_k = k.replace("'", "''")
        cond = f"(name LIKE '%{safe_k}%' OR path LIKE '%{safe_k}%' OR pinyin LIKE '%{safe_k}%')"
        name_conditions.append(cond)

    # 3. 组合 name_conditions（AND 连接）
    name_conditions_str = " AND ".join(name_conditions) if name_conditions else "1=1"

    query_data_sql = f"SELECT * FROM bookmark WHERE ({name_conditions_str}) OR url LIKE '%{url_keyword}%' order by adddate desc"
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
