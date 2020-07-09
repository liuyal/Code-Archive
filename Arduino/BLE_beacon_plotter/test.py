import serial, os, sys, time, io



a1 = serial.Serial('COM4', 115200)

a1.write('start\n'.encode())
a1.flush()
time.sleep(3)
msg1 = a1.read(a1.inWaiting())
print(msg1)

while True:
    if b"ack" in msg1:
        break
    else:
        time.sleep(1)
        a1.write('start\n'.encode())
        a1.flush()
        time.sleep(3)
        msg1 = a1.read(a1.inWaiting())
        print(msg1)


while True:
    msg1 = a1.readline()
    print(msg1)