
import os, sys,re ,time, random, thread
from multiprocessing import Process
from threading import Thread
from datetime import datetime

inmotionautomation_home_dirname = os.environ['INMOTIONAUTOMATION_HOME']
sys.path.append(inmotionautomation_home_dirname+"/lib/common")

import yaml
import basic_inmotion as bm
import proxy_airlink, ping_airlink

wan_ip = "192.168.100.1"
lan_ip = "192.168.100.2"

proxy_wan_ip = "192.168.100.3"
proxy_lan_ip = "192.168.100.5"


proxy_hostLan = proxy_airlink.ProxyAirlink(proxy_lan_ip, 18812)
host_lan = proxy_hostLan.connect()
if not host_lan: sys.exit("Test fail: Could not connect LAN side Proxy!")
else: print("LAN side Proxy connect")

proxy_hostWan = proxy_airlink.ProxyAirlink(proxy_wan_ip, 18812)
host_wan = proxy_hostWan.connect()
if not host_wan: sys.exit("Test fail: Could not connect LAN side Proxy!")
else: print("LAN side Proxy connect")

ping = ping_airlink.PingAirlink()
remote_ping_lan = proxy_hostLan.deliver(ping)
if (remote_ping_lan.ping_test(wan_ip)): print("Ping successfully")
else: print("Ping failed")

remote_ping_wan = proxy_hostWan.deliver(ping)
if (remote_ping_wan.ping_test(lan_ip)): print("Ping successfully")
else: print("Ping failed")

host_lan.execute("print('LAN connected')")
host_wan.execute("print 'WAN connected'")


print("")