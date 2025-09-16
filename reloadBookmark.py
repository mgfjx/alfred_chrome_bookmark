#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sqlite3
import json
import datetime
import sys
from define import *
sys.path.append('./lib')
from pypinyin import pinyin, lazy_pinyin, Style

def reload_bookmark(callback):
    relative_path = os.path.join(kBookmarkPath, kBookmarkName)
    bookmark_path = os.path.expanduser(relative_path)
    try:
        with open(bookmark_path, 'r', encoding='utf-8') as file:
            data = file.read()
            json_object = json.loads(data)
            callback(json_object)
    except Exception as e:
        print(e)
        callback({})

def format_timestamp(webkit_timestamp):
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(webkit_timestamp))
    utc_time = epoch_start + delta

    # 获取当前本地时区与 UTC 的差异（以小时和分钟为单位）
    # 如果是夏令时，返回的偏差会自动考虑
    local_offset = datetime.datetime.now() - datetime.datetime.utcnow()

    # 将 UTC 时间转换为本地时间
    local_time = utc_time + local_offset
    # local_time 转成：年-月-日 时:分:秒
    time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
    return time_str

def process_bookmark_node(node, path=''):
    bookmark_list = []

    node_type = node.get('type', "")
    name = node.get('name', "")

    # Update current path
    adddate = format_timestamp(node.get('date_added'))

    if node_type == "folder":
        children = node.get('children', [])
        current_path = os.path.join(path, name) if path else name
        if name == 'lsj':
            return []
        for child in children:
            bookmark_list.extend(process_bookmark_node(child, current_path))
    else:
        url = node.get('url', "")
        pinyin_str = path+name
        name_pinyin = ''.join(lazy_pinyin(pinyin_str))
        path_pinyin = ''.join(lazy_pinyin(path))
        bookmark_list.append({'name': name, 'url': url, 'path': path, 'adddate': adddate, 'pinyin': name_pinyin, 'pathpinyin': path_pinyin})

    return bookmark_list

def create_database(bookmark_list):
    if not bookmark_list:
        return

    db_path = os.path.join(kBookmarkPath, kDataBaseName)
    db_path = os.path.expanduser(db_path)

    # Remove existing database file
    if os.path.exists(db_path):
        os.remove(db_path)

    db = sqlite3.connect(db_path)
    create_table_sql = 'CREATE TABLE IF NOT EXISTS bookmark (name TEXT, path TEXT, url TEXT, adddate TEXT, pinyin TEXT, pathpinyin TEXT)'
    insert_data_sql = 'INSERT INTO bookmark (name, path, url, adddate, pinyin, pathpinyin) VALUES (?, ?, ?, ?, ?, ?)'

    # Create table
    db.execute(create_table_sql)
    for row in bookmark_list:
        data = (row['name'], row['path'], row['url'], row['adddate'], row['pinyin'], row['pathpinyin'])
        db.execute(insert_data_sql, data)

    db.commit()
    db.close()

def get_bookmark_list(json_obj):
    roots = json_obj.get('roots', {'bookmark_bar': {}})
    bookmark_bar = roots.get('bookmark_bar', {})
    bookmark_list = process_bookmark_node(bookmark_bar)
    mobile_sync = roots.get('synced', {})
    mobile_bookmark_list = process_bookmark_node(mobile_sync)
    # 合并两个列表
    bookmark_list = bookmark_list + mobile_bookmark_list
    create_database(bookmark_list)

if __name__ == '__main__':
    reload_bookmark(lambda data: get_bookmark_list(data))
