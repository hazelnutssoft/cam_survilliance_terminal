#coding=utf-8
__author__ = 'guoxiao'
import urllib2
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
        print "tab",tab
        kw = {}
        get_basic_conf_value(kw)

        positions = get_positions()
        self.render('setting.html', page_name="setting",tab = tab,positions = positions, basic_info = kw)


class apply_adding_handler(Base_Handler):
    def post(self):
        object_name = self.get_argument('object_name', '')
        position = self.get_argument('position', '')
        duration = self.get_argument('duration', 1)
        ip_address = self.get_argument('ip_address','')
        if object_name and position and duration and ip_address:
            ip_address = "rtsp://guoxiao:sonic513@%s:88/videoMain"%(ip_address)
            res = insert_position(object_name, position, str(duration), ip_address)
            if res:
                SnapshotUtil.get_instance().add_snapshot(int(position), ip_address, int(duration))
                self.write(RES_SUCCESS)
                return
            else:
                self.write(RES_FAIL)
                return
        self.write(RES_FAIL)
        return

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
                return self.write(RES_SUCCESS)
                
            else:
                return self.write(RES_FAIL)
        self.write(RES_FAIL)
        self.finish()


class operator_position_handler(Base_Handler):
    def get(self):
        operator = self.get_argument('operater', '')
        positions_d = self.get_argument('positions',[])

        positions = [str(i) for i in range(5)]
        object_names = get_object_names()
        if operator == "add":
            self.render('operate_position.html', operator=operator, positions=positions, object_names=object_names, ip_address="192.168.0.150", page_name="setting")
            return
        if operator == "edit":
            object_name = self.get_argument("object_name","");
            duration = self.get_argument("duration","");
            ip_address = self.get_argument("ip_address","");
            position = self.get_argument("position","");
            self.render('operate_position.html', operator=operator, positions=positions, object_names=object_names, page_name="setting", object_name = object_name, duration = duration, position = position,ip_address = ip_address)
            return
        if operator == "upload":
            if self.upload_positions():
                self.write(RES_SUCCESS)
                return
            else:
                self.write(RES_FAIL)
                return
        if operator == "delete":
            for pos in positions:
                delete_position(pos)
                SnapshotUtil.get_instance().remove_snapshot(int(pos))

    def upload_positions(self):
        positions = get_positions()
        url = "http://{0}:{1}{2}".format(SERVER_WEBSITE, API_PORT, POSITION_URL)
        kw = {'mac': get_mac_address(),'positions':[]}
        kw['positions'] = positions
        j_data = json.dumps(kw)
        print j_data
        req = urllib2.Request(url, j_data)
        try:
            res = urllib2.urlopen(req, timeout=30)
            print res
            if res.read().strip() == RES_SUCCESS:
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
            kw['location'] = location
            set_basic_conf_value(kw)
            if self.upload_device(location):
                self.write(RES_SUCCESS)
                return
        self.write(RES_FAIL)
        return
    def upload_device(self, location):
        url = "http://{0}:{1}{2}".format(SERVER_WEBSITE, API_PORT, DEVICE_URL)
        data = {'mac': get_mac_address(),'location':location}
        j_data = json.dumps(data)
        req = urllib2.urlopen(url, j_data)
        try:
            res = urllib2.urlopen(req, timeout=30)
            if res.read().strip() == RES_SUCCESS:
                return True
            else:
                return False
        except Exception as e:
            return False
        

class user_observer_handler(Base_Handler):
    def post(self):
        user_name = self.get_argument('user_name','')
        user_password = self.get_argument('user_password','')
        is_observed = self.get_argument('is_observed','')
        print user_name,user_password, is_observed
        if user_name and user_password and is_observed:
            print "is_observed",is_observed
            if is_observed == "true":
                is_obs = True
            else:
                is_obs = False
            mac = get_mac_address()
            data = {'mac': mac, 'observed':is_obs, 'user_name': user_name, 'user_password': user_password}
            j_data = json.dumps(data)
            url = "http://{0}:{1}{2}".format(SERVER_WEBSITE, API_PORT, OBSERVER_URL) 
            req = urllib2.Request(url, j_data)
            try:
                res = urllib2.urlopen(req, timeout=30)
                if res.read().strip() == RES_SUCCESS:
                    return self.write(RES_SUCCESS)
                else:
                    return self.write(RES_FAIL)
            except Exception as e:
                return self.write(RES_FAIL)
        return self.write(RES_FAIL)
                
