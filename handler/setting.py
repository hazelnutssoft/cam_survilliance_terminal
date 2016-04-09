#coding=utf-8
__author__ = 'guoxiao'

import tornado
from tornado.options import options
from base import Base_Handler
from util.dbtool import *
from util.snapshot import SnapshotUtil

# from util.conf import *
# import shutil
from util import *
import time

class setting_handler(Base_Handler):
    def get(self):
        tab = self.get_argument('tab',"1")
        self.render('setting.html', tab = tab)


class apply_adding_handler(Base_Handler):
    def get(self):
        object_name = self.get_argument('object_name', '')
        position = self.get_argument('position', '')
        duration = self.get_argument('duration', '')
        ip_address = self.get_argument('ip_address','')
        if object_name and position and duration and ip_address:
            res = insert_position(object_name, position, duration, ip_address)
            if res:
                SnapshotUtil.get_instance().add_snapshot(int(position), ip_address, duration)
                self.write('True')
            else:
                self.write('False')
        self.write('False')
        self.finish()


class apply_edition_handler(Base_Handler):
    def get(self):
        object_name = self.get_argument('object_name', '')
        position = self.get_argument('position', '')
        duration = self.get_argument('duration', '')
        ip_address = self.get_argument('ip_address', '')
        if object_name and position and duration and ip_address:
            res = update_position(object_name, position, duration, ip_address)
            if res:
                SnapshotUtil.get_instance().set_snapshot_interval(int(position), int(duration))
                self.write('True')
            else:
                self.write('False')
        self.write('False')
        self.finish()


class operator_position_handler(Base_Handler):
    def get(self):
        operation = self.get_argument('operator', '')
        positions = [str(i) for i in range(5)]
        object_names = get_object_names()
        if operation == "add":
            self.render('operate_position.html', operation=operation, positions=positions, object_names=object_names)
        if operation == "edit":
            self.render('operate_position.html', operation=operation, positions=positions, object_names=object_names)


class device_time_handler(Base_Handler):
    @tornado.web.asynchronous
    def get(self):
        device_time =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.write(device_time)
        self.finish()
        # self.get_data(callback=self.on_finish)
    # def get_data(self, callback):
    #     if self.request.connection.stream.closed():
    #         return
    #     device_time =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    #     callback(device_time)
    # def on_finish(self, data):

class time_synchronize_handler(Base_Handler):
    def get(self):
        time = self.get_argument('time')
        set_device_time(time)


class reboot_handler(Base_Handler):
    def get(self):
        device_reboot()