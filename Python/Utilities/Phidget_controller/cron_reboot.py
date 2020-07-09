import time, sys, os, re
import unittest, subprocess

import traceback
from Phidget22.Devices.DigitalOutput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from PhidgetHelperFunctions import *

inmotionautomation_home_dirname = os.environ['INMOTIONAUTOMATION_HOME']
sys.path.append(inmotionautomation_home_dirname + "/lib/common")
sys.path.append(inmotionautomation_home_dirname + "/lib/site-packages")

import mg_connection_wd as mg_connection

print(sys.version)

def onAttachHandler(self):
    ph = self
    try:
        print("\nAttach Event:")
        serialNumber = ph.getDeviceSerialNumber()
        channelClass = ph.getChannelClassName()
        channel = ph.getChannel()

        deviceClass = ph.getDeviceClass()
        if (deviceClass != DeviceClass.PHIDCLASS_VINT):
            print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) + "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")

    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

def onDetachHandler(self):
    ph = self
    try:
        print("\nDetach Event:")
        serialNumber = ph.getDeviceSerialNumber()
        channelClass = ph.getChannelClassName()
        channel = ph.getChannel()
        deviceClass = ph.getDeviceClass()
        if (deviceClass != DeviceClass.PHIDCLASS_VINT):
            print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) + "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

def onErrorHandler(self, errorCode, errorString):
    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

def configChannel(phi, serial, channel):
    phi.setDeviceSerialNumber(serial)
    phi.setHubPort(-1)
    phi.setIsHubPortDevice(0)
    phi.setChannel(channel)
    phi.setOnAttachHandler(onAttachHandler)
    phi.setOnDetachHandler(onDetachHandler)
    phi.setOnErrorHandler(onErrorHandler)
    try:
        phi.openWaitForAttachment(5000)
    except PhidgetException as e:
        PrintOpenErrorMessage(e, phi)
        raise EndProgramSignal("Program Terminated: Open Failed")

if __name__ == "__main__":

    Phidget_serial = 288083
    Phidget_channel = 0
    phidget = DigitalOutput()
    configChannel(phidget, Phidget_serial, Phidget_channel)
    phidget.setDutyCycle(1)

    esn = ""
    lan_ip = "172.22.0.1"
    lan_port = 2222
    usr = "root"
    pwd = "root"

    ssh = mg_connection.SSH_Connection(esn, lan_ip, lan_port, usr, pwd)

    try: ssh.login()
    except: print("SSH ERROR")

    ssh.ssh_sendline("cat /etc/issue")
    msg = ssh.ssh_read()[1]
    cnt = 0

    while True:

        while True:
            try:
                if ssh.login() != -1:break
                else:print("Connection to device failed, retry...")
            except: None
            time.sleep(10)

        while True:
            print("Restart batchlogger")
            shell = ssh.start_command("batchlogger restart")
            time.sleep(5)
            ssh.ssh_sendline("ps -ef | grep batch")
            ps_msg = ssh.ssh_read(1)[1]
            if "batchlogger restart" not in ps_msg: print("batchlogger not found...")

            ssh.ssh_send("date +%Y-%m-%d\r")
            date = ssh.ssh_read(2)[1].split('\r\n')
            date_set = ""
            for x in date:
                if bool(re.match('[\d/-]+$', x)): date_set = x ;break
            ssh.ssh_sendline("tail /opt/inmotiontechnology/logs/"+date_set+"batchlogger.log")
            log_msg = ssh.ssh_read(1)[1]
            print(log_msg)
            print("check sleep time < 10")
            for i, line in reversed(list(enumerate(log_msg.split('\r\n')))):
                if "sleeps" in line: time_sleep = line.split(' ')[line.split(' ').index("sleeps")+1]; break
            if int(time_sleep) < 10: print("sleep time: "+str(time_sleep)+" less than 10min"); break
            else: print("sleep time: "+str(time_sleep)+" restart batchlogger");ssh.end_command(shell)
            time.sleep(1)

        print("sleep for "+str(time_sleep)+ "min")
        time.sleep(int(time_sleep)*60+5)

        ssh.ssh_send("date +%Y-%m-%d\r")
        date = ssh.ssh_read(2)[1].split('\r\n')
        date_set = ""
        for x in date:
            if bool(re.match('[\d/-]+$', x)): date_set = x; break
        ssh.ssh_sendline("tail /opt/inmotiontechnology/logs/" + date_set + "batchlogger.log")
        log_msg = ssh.ssh_read(1)[1]
        print(log_msg)
        if "batchlogger completed." not in log_msg: sys.exit("batch logger failed to complete")

        ssh.end_command(shell)
        time.sleep(5)
        print("Power off")
        phidget.setDutyCycle(0)
        print("sleep for 20")
        time.sleep(20)
        print("Power on")
        phidget.setDutyCycle(1)
        time.sleep(90)
        cnt += 1
        print("End Cyle " + str(cnt))
