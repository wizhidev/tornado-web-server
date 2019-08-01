#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-08-01 10:40
# @Author  : wizhi
# @Site    : logs
# @File    : LogsDo.py
from library.MyMongodb import MyMongo


class LogsModel(MyMongo):
    _fields = {
        'request_id': (str, True),
        'keyword': (str, True),
        'data': (str, True),
    }

    def __init__(self, **kwargs):
        super().__init__('logs', **kwargs)