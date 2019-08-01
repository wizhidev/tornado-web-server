#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-08-01 09:28
# @Author  : wizhi
# @Site    : mongodb
# @File    : MyMongodb.py

from pymongo import MongoClient
from datetime import datetime

from library.Exception import CustomException


class MyMongo(object):
    """ mongodb 连接 """

    _instance = None

    def __init__(self, dsn=None, dbname=None):
        self.dsn = dsn
        self._mongodb_client = None
        self.dbname = dbname

    @classmethod
    def getInstance(cls, dsn=None, dbname=None):
        if cls._instance is None:
            cls._instance = cls(dsn=dsn, dbname=dbname)
        return cls._instance

    def close(self):
        if self._mongodb_client is not None:
            self._mongodb_client.close()

    @property
    def get_mongodb_client(self):
        if self._mongodb_client is None:
            self._mongodb_client = MongoClient(self.dsn)
        return self._mongodb_client[self.dbname]

    def create(self, mongo, doc_or_docs):
        """插入文档
        相比于MongoDB原生的insert，增加了none值字段过滤和模型字段验证。

        :Parameters:
          - `doc_or_docs`: ``dict`` or ``list``，单个文档或文档列表

        :Returns:
          - 同原生insert接口
        """
        if isinstance(doc_or_docs, dict):
            self._filter_none_value(doc_or_docs)
            self._validate(doc_or_docs)
            if 'create_time' not in doc_or_docs:
                doc_or_docs['create_time'] = datetime.now()
            doc_or_docs['update_time'] = doc_or_docs['create_time']
            ret = mongo['test'].insert_one(doc_or_docs)
            # ret = super().insert_one(doc_or_docs)
            return ret.inserted_id
        elif isinstance(doc_or_docs, list):
            for v in doc_or_docs:
                self._filter_none_value(v)
                self._validate(v)
                if 'create_time' not in v:
                    v['create_time'] = datetime.now()
                v['update_time'] = v['create_time']
            ret = super().insert_many(doc_or_docs)
            return ret.inserted_ids

    @staticmethod
    def _filter_none_value(doc):
        if not isinstance(doc, dict):
            raise CustomException(code=10001, desc="doc should be a dict")

        for k, v in list(doc.items()):
            if v is None:
                del doc[k]

        return doc

    @classmethod
    def _validate(cls, doc, required=True):
        if cls._fields is None:
            return

        for k, v in doc.items():
            if '.' in k:
                continue

            if k not in cls._fields:
                raise CustomException(code=10001, desc='unexpected field {}'.format(k))

            type_, _ = cls._fields[k]
            if type_ is not None and not isinstance(v, type_):
                raise CustomException(code=10001, desc='field {} should be a {}'.format(k, type_))

        if required:
            fields = [k for k, v in cls._fields.items() if v[1]]
            for v in fields:
                if v not in doc:
                    raise CustomException(code=10001, desc='field {} is required'.format(v))
