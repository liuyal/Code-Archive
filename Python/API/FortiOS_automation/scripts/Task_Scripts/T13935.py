import os
import re
import sys
import time
import json
import urllib3
import datetime
import threading

from testscript.libs.dev.ljerry.fgt_diagnose.system import ha as Diag_HA

from testscript.libs.fgtcli.fgtcli import FGT
from atp_main import LOG


def flush_ike(logger, fgt):
    fgt_m = FGT(logger=logger, ip=fgt['ip'])
    fgt_m.create_ssh_client()
    result = fgt_m.run_cmd('c v\ned hub1\nd vpn ike gateway flush')
    fgt_m.end_session()

def check_kernel_route(logger, fgt):
    fgt_m = FGT(logger=logger, ip=fgt['ip'])
    fgt_m.create_ssh_client()
    result = fgt_m.run_cmd('c v\ned hub1\nd ip route list')
    fgt_m.end_session()


def set_ha_order(logger, master, slave, timeout=2 * 60):
    start_time = time.time()
    in_order = False
    synced = False

    while True:

        fgt_m = FGT(logger=logger, ip=master['ip'])
        fgt_m.create_ssh_client()
        result = fgt_m.run_cmd('c g\ng sys ha status')
        fgt_m.end_session()

        ha_status = Diag_HA.Status(result)
        master_serial = fgt_m.system_status['serial_number']
        for order in ha_status.ha_order:
            if order['role'] == "Primary" and order['serial'] == master_serial:
                in_order = True
            else:
                fgt_s = FGT(logger=logger, ip=slave['ip'])
                fgt_s.create_ssh_client()
                fgt_s.run_cmd('c g\nexecute ha failover set 1\ny', sleep=10)
                fgt_s.end_session()

        count = []
        for status in ha_status.configuration_status:
            count.append(status['status'])
            if status['status'] != 'in-sync':
                fgt_s = FGT(logger=logger, ip=slave['ip'])
                fgt_s.create_ssh_client()
                fgt_s.run_cmd('c g\nexec ha synchronize start', sleep=5)
                fgt_s.end_session()
                fgt_m = FGT(logger=logger, ip=master['ip'])
                fgt_m.create_ssh_client()
                fgt_m.run_cmd('c g\nexec ha synchronize start', sleep=5)
                fgt_m.end_session()

        if count.count('in-sync') == 2:
            synced = True

        if in_order and synced:
            for order in ha_status.ha_order:
                logger.info(order['role'] + " " + order['hostname'] + " " + order['serial'])
            break

        if time.time() - start_time > timeout:
            raise Exception("HA did not sync within time out")

if __name__ == "__main__":
    master = {'ip': '172.18.10.61'}
    slave = {'ip': '172.18.10.62'}

    set_ha_order(LOG(), master, slave)

    flush_ike(LOG(), master)

    time.sleep(5)
    print('')

    set_ha_order(LOG(), slave, master)

    flush_ike(LOG(), slave)

    time.sleep(5)
    print('')