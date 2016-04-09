#!/usr/bin/env python
# coding=utf-8

import os
import sys
import tornado.web
import tornado.ioloop
from handler import *
import tornado.options
from tornado.options import define,options
tornado.options.parse_command_line()

import routes
from util.snapshot import SnapshotUtil

define('port', default = 8888, type = int, help = 'app listen port')
define('debug', default = True, type = bool, help = 'is debuging?')

options.log_file_prefix = 'log/www/web.log'
options.logging = 'debug' if options.debug else 'info'

def create_app():
    settings = {
        'static_path':'static',
        'template_path':'template',
        'xsrf_cookies':False,
        'debug': options.debug,
    }
    return tornado.web.Application(routes.handlers, **settings)

if __name__ == "__main__":
    app = create_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    SnapshotUtil.get_instance().snapshot_start()