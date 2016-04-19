__author__ = 'guoxiao'
import os
import socket
import fcntl
import struct
import shutil
import md5
import uuid

from snapshot import *
from marcos import *
from dbtool import *
import ConfigParser
import subprocess



def get_pwd_dir():
    return os.getcwd()

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_mac_address():
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return mac

def get_md5(raw_str):
    mdtool = md5.new()
    mdtool.update(raw_str)
    return mdtool.hexdigest()

def disk_stat():
    hd={}
    disk = os.statvfs("/")
    hd['available'] = (disk.f_bsize * disk.f_bavail)/(1024*1024*1024)
    hd['capacity'] = (disk.f_bsize * disk.f_blocks)/(1024*1024*1024)
    hd['used'] = hd['capacity']-hd['available']
    return hd

def clear_data():
    pwd = get_pwd_dir()
    captured_dir = os.path.join(pwd, CAPTURED_DIR)
    thunmbnail_dir = os.path.join(pwd, THUMBNAIL_DIR)


    if os.path.isdir(thunmbnail_dir):
        shutil.rmtree(thunmbnail_dir)
    if os.path.isdir(captured_dir):
        shutil.rmtree(captured_dir)
    db_truncate()

def get_object_names():
    conf_dir = get_pwd_dir() + '/conf/object_names.ini'
    config = ConfigParser.ConfigParser()
    config.read(conf_dir)
    object_names_str = config.get('objects', 'names')
    object_names = object_names_str.split(',')
    return object_names

def get_basic_conf_value(kw):
    # conf_dir = os.path.join(get_pwd_dir(), '/conf/device_conf.ini')
    conf_dir = get_pwd_dir() + '/conf/device_conf.ini'
    # print conf_dir
    read_conf(conf_dir, kw)
    kw['storage'] = str(disk_stat()['available'])
    kw['used_storage'] = str(disk_stat()['used'])
    # return

def set_basic_conf_value(kw):
    conf_dir = get_pwd_dir()+'/conf/device_conf.ini'
    # print conf_dir
    write_conf(conf_dir, kw)
    # kw['storage'] = str(disk_stat()['available'])

def read_conf(conf_dir, kw):
    config = ConfigParser.ConfigParser()
    config.read(conf_dir)
    kw['location'] = config.get('dev', 'location')

def write_conf(conf_dir, kw):
    config = ConfigParser.ConfigParser()
    # print conf_dir
    config.read(conf_dir)
    fp = open(conf_dir, 'w')
    # print kw['device_name']
    # print kw['device_id']
    config.set('dev', 'location', kw['location'])
    # device_type = config.get('conf', 'device_type')
    # channel_number = config.get('conf', 'channel_number')
    print config
    config.write(fp)
    fp.close()

def set_device_time(time_str):
    command = "sudo date -s "+"\""+time_str+"\""
    print command
    os.system(command)

def device_reboot():
    # print 'device reboot'
    subprocess.Popen('sudo reboot', shell=True, stdout=subprocess.PIPE)
