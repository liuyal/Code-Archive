import time, sys, os, re
import unittest, subprocess

import traceback
from Phidget22.Devices.DigitalOutput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from PhidgetHelperFunctions import *


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

    Phidget_serial = 383808
    Phidget_channel = 0
    phidget = DigitalOutput()
    configChannel(phidget, Phidget_serial, Phidget_channel)
    phidget.setDutyCycle(1)

    while True:
        time.sleep(5)
        phidget.setDutyCycle(0)
        time.sleep(5)
        phidget.setDutyCycle(1)

