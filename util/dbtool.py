#!/usr/bin/env python
# coding=utf-8


__author__ = 'guoxiao'


import mysql.connector
import time

from marcos import *

def create_engine(user, password, database, is_auto_commit=False, host='127.0.0.1', port=3306, **kw):
    params = dict(user=user, password=password, database=database, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=is_auto_commit)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    params.update(kw)
    params['buffered'] = True
    engine = mysql.connector.connect(**params)
    return engine


def create_nowTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def create_nowTime_strip():
    return time.strftime('%Y%m%d%H%M%S', time.localtime())

class database_resource:
    def __enter__(self):
        self.conn = create_engine(DB_USER, DB_USER_PASSWORD, DB_NAME, is_auto_commit=True)
        self.cursor = self.conn.cursor()
        return self.cursor
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


def add_caputured_image(filename, position, width, height):
    with database_resource() as cursor:
        sqlstr = 'insert into %s (image_path, position, created_at, width, height)'%(DB_IAMGE_TABLE_NAME)
        sqlstr = sqlstr+'values (%s, %s, %s, %s, %s)'
        res = cursor.execute(sqlstr,[filename, position, create_nowTime(), width, height])
        if res > 0:
            return True
        else:
            return False


def get_images(limit, offset, position):
    # with database_resource():
    conn = create_engine(DB_USER, DB_USER_PASSWORD, DB_NAME, is_auto_commit=True)
    cursor = conn.cursor(dictionary=True)
    sqlstr = "select * from %s where position = %d order by id desc limit %s offset %s"%(DB_IAMGE_TABLE_NAME, position, limit, offset)
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    return result


def get_images_count(position):
    with database_resource() as cursor:
        cursor.execute("select count(id) from %s where position = %d"%(DB_IAMGE_TABLE_NAME, position))
        res = cursor.fetchall()[0][0]
        return int(res)


def insert_position(object_name, position, duration, ip_address):
    with database_resource() as cursor:
        sqlstr = 'insert into %s (object_name, position, duration, ip_address)' % (DB_POSITION_TABLE_NAME)
        sqlstr = sqlstr+ 'values (%s, %s, %s, %s)'
        res = cursor.execute(sqlstr, [object_name, position, duration, ip_address])
        if res >0:
            return True
        else:
            return False

def update_position(object_name, position, duration, ip_address):
    with database_resource() as cursor:
        sqlstr = 'update %s set object_name = %s, duration=%s, ip_address=%s where position = %s' % (DB_POSITION_TABLE_NAME, object_name, duration, ip_address, position)
        res = cursor.execute(sqlstr)
        if res > 0:
            return True
        else:
            return False


def get_positions():
    conn = create_engine(DB_USER, DB_USER_PASSWORD, DB_NAME, is_auto_commit=True)
    cursor = conn.cursor(dictionary=True)
    sqlstr = "select * from %s"%(DB_POSITION_TABLE_NAME)
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    return result



def db_truncate():
    with database_resource() as cursor:
        cursor.execute("truncate %s"%DB_IAMGE_TABLE_NAME)

