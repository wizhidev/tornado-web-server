#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json

from tornado.web import RequestHandler
from library.Exception import CustomException
from library.G import G
from library.Result import Result
from library.Utils import Utils


class BaseHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    uid = None
    token = None

    def compute_etag(self):
        """ 取消缓存 """
        return None

    def write_error(self, status_code, **kwargs):
        if isinstance(kwargs.get('exc_info')[1], CustomException):
            ce = kwargs.get('exc_info')[1]
            self.set_status(200)
            return self.json(Result(code=ce.code, msg=ce.msg))
        else:
            return self.json(Result(code=status_code, msg="未知错误"))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "X-Token, Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def on_finish(self):
        """ 清理资源 """
        G.getInstance().clear()

    def json(self, result):
        self.write(json.dumps(result.json(), cls=Utils.JSONEncoder(), sort_keys=False))
        self.finish()

    def options(self, *args, **kwargs):
        self.set_status(204)
