__author__ = 'guoxiao'
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import os
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
from marcos import *
from commons import *
from dbtool import add_caputured_image,get_positions
import time

register_openers()

class SnapshotUtil(object):
    instance = None

    def __init__(self):
        self.scheduler = TornadoScheduler()
    @staticmethod
    def get_instance():
        if not SnapshotUtil.instance:
            SnapshotUtil.instance = SnapshotUtil()
        return SnapshotUtil.instance


    def set_snapshot_interval(self, pos, hours):
        self.scheduler.reschedule_job('snapshot_%d' % pos, trigger='interval', hours=hours)


    def snapshot_start(self):
        self.scheduler.start()


    def snapshot_stop(self):
        self.scheduler.shutdown()

    def snapshot(self, pos, url):
        print "snapshot",pos,url
        path = os.path.join(os.getcwd(),CAPTURED_DIR)
        path = os.path.join(path, str(pos)+"_"+time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(time.time()))+".jpeg")
        command = "sudo ffmpeg -ss 30 -i \'%s\' -y -t 30 -r 1 -f image2 %s" % (url, path)
        print command
        os.system(command)
        time.sleep(5)
        add_caputured_image(os.path.basename(path), pos, 1920, 1080)
        self.update_image(path, pos)


    def update_image(self, path, pos):
        datagen, headers = multipart_encode({'file': open(path, "rb"), 'pos': pos, "mac": get_mac_address(),'created_at': time.time()})
        url = 'http://%s:%d%s'%(SERVER_WEBSITE, API_PORT, UPLOAD_IMG_URL)
        print url
        request = urllib2.Request(url, datagen, headers)
        res = urllib2.urlopen(request, timeout=30).read()
        print "ok"
        if res == "ok":
            return
        else:
            return

    def remove_snapshot(self,pos):
        self.scheduler.remove_job("snapshot_%d"%pos)

    def add_snapshot(self, pos, url, hours):
        self.scheduler.add_job(self.snapshot, 'interval', args=[ pos, url], seconds=100, id="snapshot_%d"%(pos))

    def init_snapshot(self):
        positions = get_positions()
        for pos in positions:
            self.add_snapshot(int(pos['position']), pos['ip_address'], pos['duration'])

if __name__=="__main__":
    sp = SnapshotUtil.get_instance()
    #sp.get_instance().snapshot(args={'pos':0, 'url':'rtsp://guoxiao:sonic513@192.168.0.150:88/videoMain'})
    sp.get_instance().add_snapshot(0,url='rtsp://guoxiao:sonic513@192.168.0.150:88/videoMain',hours=1)
    sp.get_instance().snapshot_start()
    a = raw_input("wait for the apscheduler!, press any key to quit")
    #sp.update_image('/home/pi/cam_survilliance_terminal/static/img/captured/0_2016_04_14_08_36_18.jpeg',0)
