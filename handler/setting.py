#coding=utf-8
__author__ = 'guoxiao'

import tornado
from tornado.options import options
from base import Base_Handler
from util.dbtool import *
from util.snapshot import SnapshotUtil
import json
# from util.conf import *
# import shutil
from util import *
import time
from util.marcos import *

class setting_handler(Base_Handler):
    def get(self):
        tab = self.get_argument('tab',"1")
        positions = get_positions()
        self.render('setting.html', page_name="setting",tab = tab,positions = positions)


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
        operator = self.get_argument('operater', '')

        positions = [str(i) for i in range(5)]
        object_names = get_object_names()
        if operator == "add":
            self.render('operate_position.html', operator=operator, positions=positions, object_names=object_names, page_name="setting")
            return
        if operator == "edit":
            self.render('operate_position.html', operator=operator, positions=positions, object_names=object_names, page_name="setting")
            return
        if operator == "upload":
            return self.upload_positions()

    def upload_positions(self):
        positions = get_positions()
        url = "http://{0}:{1}{2}".format(SERVER_WEBSITE, API_PORT, DEVICE_URL)
        j_data = json.dumps(positions)
        req = urllib2.Request(url, j_data)
        try:
            res = urllib2.urlopen(req, timeout=30)
            if res.read().strip() == RES_SUCESS:
                return True
            else:
                return False
        except Exception as e:
            return False


class device_time_handler(Base_Handler):
    @tornado.web.asynchronous
    def get(self):
        device_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
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


class device_location_handler(Base_Handler):
    def get(self):
        location = self.get_argument('location','')
        if location:
            kw = {}
            get_basic_conf_value(kw)
            kw['device_location'] = location
            set_basic_conf_value(kw)
            self.write("ok")
            return
        self.write("fail")
        return