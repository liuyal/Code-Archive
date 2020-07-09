import time, os, sys, datetime
import serial

serial_com = "COM3"
baud_rate = 9600
connection = serial.Serial(serial_com, baudrate=baud_rate, timeout=30)

f = open("log.txt", "a")
f.truncate(0)
try:
    while True:
        line = connection.readline()
        if line != b"":
            print(line.decode(encoding='UTF-8', errors='ignore').strip())
            f.write(line.decode(encoding='UTF-8', errors='ignore').strip() + "\n")
            f.flush()
except Exception as e:
    print(e)
    f.close()
