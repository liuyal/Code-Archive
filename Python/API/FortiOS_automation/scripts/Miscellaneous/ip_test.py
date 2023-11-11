import os
import re
import sys
import time
import json
import urllib3
import datetime
import threading



if __name__ == "__main__":

    f = open('ip.txt', 'r')
    text = f.readlines()
    f.close()

    ip_list = {}
    ip_list['1.1.0.0'] = {}
    ip_list['3.3.0.0'] = {}

    for line in text:
        if line.count('.') >= 3 and '1.1.' == line.split()[0][0:4]:

            ip = line.split()[0]

            if ip.split('.')[2] not in ip_list['1.1.0.0']:
                ip_list['1.1.0.0'][ip.split('.')[2]] = []

            ip_list['1.1.0.0'][ip.split('.')[2]].append(ip)

        elif line.count('.') >= 3 and '3.3.' == line.split()[0][0:4]:
            ip = line.split()[0]

            if ip.split('.')[2] not in ip_list['3.3.0.0']:
                ip_list['3.3.0.0'][ip.split('.')[2]] = []

            ip_list['3.3.0.0'][ip.split('.')[2]].append(ip)

    print()