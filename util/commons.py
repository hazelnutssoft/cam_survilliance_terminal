import fcntl
import struct
import shutil
import md5
import uuid



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

