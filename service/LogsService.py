#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-08-01 10:43
# @Author  : wizhi
# @Site    : 日志服务文件
# @File    : LogsService.py
import pymongo
import re

from conf import log
from library.Exception import LogsException
from mapper.LogsDo import LogsModel
from service.BaseService import BaseService


class LogsService(BaseService):
    def register_logs(self, request_id, keyword, data):
        doc = {
            'request_id': request_id,
            'keyword': keyword,
            'data': data,
        }
        try:
            LogsModel().create(self.mongo, doc)
        except pymongo.errors.DuplicateKeyError:
            raise LogsException(code=14000, desc="资源重复")

    def logs_list(self, keyword=None, skip=0, limit=10, sort='create_time_desc'):
        spec = {}
        if keyword is not None:
            spec['keyword'] = {
                '$regex': r'\s*'.join(re.sub(r'\s+', '', keyword)),
                '$options': 'i'
            }
        spec = spec or None

        s = []
        if sort == 'create_time_desc':
            s.append(('create_time', pymongo.DESCENDING))
        elif sort == 'create_time_asc':
            s.append(('create_time', pymongo.ASCENDING))
        s = s or None

        cursor = LogsModel().find(spec, skip=skip, limit=limit, sort=s)

        return list(cursor), cursor.count()
