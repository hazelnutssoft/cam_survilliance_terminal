#coding=utf-8
__author__ = 'guoxiao'
import tornado
from tornado.options import options
import tornado.web

class Base_Handler(tornado.web.RequestHandler):

    def send_error_json(self, data):
        return self.write({
            'status': 'error',
            'content': data
            })

    def send_success_json(self, **data):
        return self.write({
            'status': 'ok',
            'content': data
            })

    @property
    def is_ajax_request(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'