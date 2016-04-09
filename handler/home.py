#coding=utf-8
__author__ = 'guoxiao'


import logging
import tornado
from tornado.options import options
from util import *
from base import Base_Handler
from util import dbtool
class AboutHandler(Base_Handler):
    def get(self):
        return self.render('about.html')


class home_handler(Base_Handler):
    def get(self):
        kw = {}
        get_basic_conf_value(kw)
        positions = dbtool.get_positions()
        for pos in positions:
            image_count = dbtool.get_images_count(pos.position)
            pos['image_count'] = image_count if image_count else 0


        return self.render('home.html',
                           page_name='home',
                           basic_info=kw,
                           positions=positions
                           )