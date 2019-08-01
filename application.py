#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado
from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from library.Urls import route
from controllers.Error import NotFoundHandler
from conf import conf, log
from oslo_context import context


class Application(web.Application):
    def __init__(self):
        settings = dict(
            debug=conf.debug,
            autoreload=conf.debug,
            default_handler_class=NotFoundHandler,
            compress_response=False
        )

        super(Application, self).__init__(route.get_urls(), **settings)


if __name__ == '__main__':
    log.info("http server start, Ctrl + C to stop...")

    context.RequestContext()
    http_server = HTTPServer(Application(), xheaders=True)
    http_server.listen(conf.port)
    tornado.ioloop.IOLoop.instance().start()
