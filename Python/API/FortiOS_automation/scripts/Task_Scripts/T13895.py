import os
import re
import sys
import time
import datetime

from pathlib import Path
from testscript.libs.utilities.ssh import SSH
from testscript.libs.fgtcli.fgtcli import FGT
from atp_main import LOG

logger = LOG()
idrsa = str(Path.home()) + os.sep + ".ssh" + os.sep + "id_rsa"
namets = datetime.datetime.now().strftime("%y%m%d_%H%M%S")


def log(text):
    if not os.path.exists(os.getcwd() + os.sep + "T13895_log"): os.mkdir(os.getcwd() + os.sep + "T13895_log")
    f = open(os.getcwd() + os.sep + "T13895_log" + os.sep + namets + "_T13895_log.txt", 'a+')
    print('[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + text + '\n')
    f.write('[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + text + '\n')
    f.flush()
    f.close()


def add_tc():
    log("Add tc delay")
    # cmd = 'echo 1234 | sudo -S tc qdisc add dev ens192.12 root netem delay 100ms'
    # cmd = 'echo 1234 | sudo -S ip route del 10.0.0.0/8 via 170.12.1.1 dev ens192.12'
    # pc = SSH(logger, host_ip='10.59.71.202', username='ubuntu202', password='1234')
    # pc.exec_cmd(cmd)
    # pc.close()

    cmd = 'c sys int\ned port3\nset status down\nnext\ned port4\nset status down\nnext\ned port5\nset status down\nnext\nend\n'
    fgt = FGT(logger=logger, ip='10.59.71.88', vdom='hub1')
    fgt.create_ssh_client()
    fgt.run_cmd(cmd)
    fgt.end_session()



def remove_tc():
    log("Remove tc delay")
    # cmd = 'echo 1234 | sudo -S tc qdisc del dev ens192.12 root'
    # cmd = 'echo 1234 | sudo -S ip route add 10.0.0.0/8 via 170.12.1.1 dev ens192.12'
    # pc = SSH(logger, host_ip='10.59.71.202', username='ubuntu202', password='1234')
    # pc.exec_cmd(cmd)
    # pc.close()
    cmd = 'c sys int\ned port3\nset status up\nnext\ned port4\nset status up\nnext\ned port5\nset status up\nnext\nend\n'
    fgt = FGT(logger=logger, ip='10.59.71.88', vdom='hub1')
    fgt.create_ssh_client()
    fgt.run_cmd(cmd)
    fgt.end_session()


def check_fgt():
    fgt = FGT(logger=logger, ip='10.59.71.86', vdom='spoke1')
    fgt.create_ssh_client()

    log("Check sdwan health-check")
    cmd = 'd sys virtual-wan-link health-check'
    output = fgt.run_cmd(cmd)
    log(output)

    log("Check sdwan service")
    cmd = 'd sys virtual-wan-link service'
    output = fgt.run_cmd(cmd)
    log(output)

    log("Check sdwan proute")
    cmd = 'd firewall proute list'
    output = fgt.run_cmd(cmd)
    log(output)

    log("Check sdwan route tag")
    cmd = 'd sys virtual-wan-link route-tag-list'
    output = fgt.run_cmd(cmd)
    log(output)

    fgt.end_session()


def wait(s):
    log('Sleep for ' + str(s))
    time.sleep(s)


if __name__ == "__main__":

    while True:
        try:
            remove_tc()
            wait(300)
            check_fgt()
            wait(10)
            add_tc()
            wait(300)
            check_fgt()
            wait(10)
        except:
            log("ERROR")
            pass
