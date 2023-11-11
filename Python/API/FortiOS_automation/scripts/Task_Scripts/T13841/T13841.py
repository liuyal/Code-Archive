import os
import time
import queue
import random
import threading

from testscript.libs.fgtcli.fgtcli import FGT
from atp_main import LOG

logger = LOG()


def flush(a, v):
    while True:
        try:
            logger.info('Flush tunnel')
            fgt27 = FGT(logger, ip='172.18.9.27')
            fgt27.create_ssh_client()
            fgt27.run_cmd('d vpn t flush')
            time.sleep(5 * 60)
            out = fgt27.run_cmd('g router info routing-table all')
            out2 = fgt27.run_cmd('diag vpn ike gateway list | grep _0 -c')
            logger.info(out + '\n')
            logger.info('# of _0: ' + out2 + '\n')
            fgt27.end_session()

        except:
            pass


def ping(a, v):
    while True:
        for i in range(1, 10):
            try:
                logger.info('Ping from ' + 'vdom' + str(i))
                fgt = FGT(logger, ip='172.18.9.127', vdom='vdom' + str(i))
                fgt.create_ssh_client()
                fgt.run_cmd('exec ping-option source 172.1.+0.1\nexec ping-option repeat-count 1\nexec ping 162.1.1.1'.replace('+', str(i)))
                fgt.end_session()
            except:
                pass
        time.sleep(3 * 60)


def ping2(a, v):
    while True:
        try:
            logger.info('Ping from ' + 'dut')
            fgt = FGT(logger, ip='172.18.9.127')
            fgt.create_ssh_client()
            for i in range(1, 10):
                fgt.run_cmd('exec ping-option source 162.1.1.1\nexec ping-option repeat-count 1\nexec ping 172.1.+0.1'.replace('+', str(i)))
            fgt.end_session()
            time.sleep(10 * 60)
        except:
            pass


if __name__ == "__main__":

    t1 = threading.Thread(target=flush, args=(1, 1))
    t2 = threading.Thread(target=ping, args=(1, 2))
    t3 = threading.Thread(target=ping2, args=(1, 2))
    thread_list = [t1, t2, t3]
    for item in thread_list: item.start()
    for item in thread_list: item.join()
