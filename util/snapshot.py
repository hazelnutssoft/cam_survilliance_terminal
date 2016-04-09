__author__ = 'guoxiao'
from apscheduler.schedulers.tornado import TornadoScheduler
import os
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
from util import *
from marcos import *
from dbtool import add_caputured_image


register_openers()

class SnapshotUtil(object):
    instance = None

    def __init__(self):
        self.scheduler = TornadoScheduler()

    def get_instance(self):
        if not self.instance:
            self.instance = SnapshotUtil()
        return self.instance


    def set_snapshot_interval(self, pos, hours):
        self.scheduler.reschedule_job('snapshot_%d' % pos, trigger='interval', hours=hours)


    def snapshot_start(self):
        self.scheduler.start()


    def snapshot_stop(self):
        self.scheduler.shutdown()

    def snapshot(self, args):
        pos = args['pos']
        url = args['url']
        path = ""
        command = "sudo ffmpeg -ss 10 -i \'%s\' -y -t 10 -r 1 -f image2 %s" % (url, path)
        os.system(command)
        time.sleep(5)
        add_caputured_image(path, pos, 1920, 1080)
        self.update_image(path, pos)


    def update_image(self, path, pos):
        datagen, headers = multipart_encode({'file': open(path, "rb"), 'pos': pos, "mac": get_md5(get_mac_address())})
        request = urllib2.Request('http://%s:%d%s'%(SERVER_WEBSITE, API_PORT, UPLOAD_IMG_URL), datagen, headers)
        res = urllib2.urlopen(request, timeout=30).read()
        if res == "ok":
            return
        else:
            return


    def add_snapshot(self, pos, url, hours):
        self.scheduler.add_job(self.snapshot, 'interval', args={'pos': pos, 'url': url}, hours=hours, id="snapshot_%d"%(pos))


