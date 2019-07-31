#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-31 16:03
# @Author  : wizhi
# @Site    : 表单字段验证
# @File    : forms.py

import formencode
from formencode import validators


class BaseForm(formencode.Schema):
    """
    by Felinx Lee
    https://bitbucket.org/felinx/poweredsites/src/8448db5ba387/poweredsites/forms/base.py
    """
    allow_extra_fields = True
    filter_extra_fields = True

    # _xsrf = validators.PlainText(not_empty=True, max=32)

    def __init__(self, handler):

        self._parmas = {}
        self._values = {}
        self._form_errors = {}

        # re-parse qs, keep_blankvalues for formencode to validate
        # so formencode not_empty setting work.
        request = handler.request
        arguments = dict((k, v[-1].decode()) for k, v in request.arguments.items())
        print(arguments)

        for k, v in arguments.items():
            if len(v) == 1:
                self._parmas[k] = v[0]
            else:
                # keep a list of values as list (or set)
                self._parmas[k] = v

        self._handler = handler
        self._result = True

    def validate(self):
        try:
            self._values = self.to_python(self._parmas)
            self._result = True
            self.__after__()
        except formencode.Invalid as error:
            print(error)
            self._values = error.value
            self._form_errors = error.error_dict or {}
            self._result = False

        # map values to define form propertys and decode utf8
        for k in self._values.keys():
            exec("self.%s = self._values[\"%s\"]" % (k, k))

        return self._result

    # add custom error msg
    def add_error(self, attr, msg):
        self._result = False
        self._form_errors[attr] = msg

    # post process hook
    def __after__(self):
        pass


class UserLoginForm(BaseForm):
    username = validators.String(not_empty=True)
    password = validators.String(not_empty=True)
