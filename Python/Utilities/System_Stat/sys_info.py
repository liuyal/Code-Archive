import os
import sys
import time
import datetime
import wmi

if __name__ == "__main__":

    w = wmi.WMI(namespace=r"root\OpenHardwareMonitor")

    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
        if sensor.SensorType == u'Temperature':
            print(sensor.Name)
            print(sensor.Value)
