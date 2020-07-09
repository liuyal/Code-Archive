import serial

ser =  serial.Serial('COM3', 9600, timeout=10)
while True:
    line = ser.readline()
    if line != b"": print(line)