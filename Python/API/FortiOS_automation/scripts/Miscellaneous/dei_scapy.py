import os
import sys
import time
from scapy import *

if __name__ == "__main__":

    ip = "13.1.1.10"

    icmp = Ether(dst="00:0c:29:1a:56:44", src="00:0c:29:65:a6:bf")/ Dot1Q(vlan=11, id=1, prio=0) / IP(dst="13.1.1.10") / ICMP()

    icmp.show2()

    ls(icmp)

    resp = sendp(icmp)

    send(IP(dst="13.1.1.10") / ICMP())