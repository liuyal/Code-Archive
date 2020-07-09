import time, os, sys, serial, glob, re, subprocess
from termcolor import colored

def List_serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    print("\nUSB Ports Detected:"); print(result); print('')
    return result

def find_USB_port(serial_ports):
    print colored("Searching for usable USB ports...","green") #Available text colors: red, green, yellow, blue, magenta, cyan, white.
    port_name = []
    for port in serial_ports:
        # print("Connecting to: " + port)
        ser = serial.Serial(port=port, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=10, writeTimeout=5)
        bytesToRead = ser.inWaiting()
        try:
            ser.write('\r'); time.sleep(1)
            ser.write('\r'); time.sleep(1)
            bytesToRead = ser.inWaiting()
            msg = ser.read(bytesToRead)
            # print(msg)
            if "ND" and "login" in msg:
                port_name.append(port)
                # print("USB Port is available")
            elif "root@" in msg:
                port_name.append(port)
                # print("USB Port is available")
        except:
            None; # print("ERROR: Closing port\n")
        ser.close()

    print colored("Usable USB ports: " + str(port_name), "green")
    return port_name

def list_usable_USB():
    serial_ports = List_serial_ports()
    good_ports = find_USB_port(serial_ports)
    return good_ports

def list_esn(input_ports):
    esn_list = []
    for port in input_ports:
        ser = serial.Serial(port=port, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=10, writeTimeout=5)
        try:
            ser.write('\r'); time.sleep(1)
            ser.write('\r');time.sleep(1)
            bytesToRead = ser.inWaiting()
            msg = ser.read(bytesToRead).split('\n')
            for line in msg:
                if "ND" and "login:"in line:
                    esn = line.split(' ')[0]
                    esn_list.append(esn.replace('\r',''))
                    break
                elif "root" in line:
                    m = re.search('@(.+?):', line)
                    if m: esn = m.group(1)
                    esn_list.append(esn)
                    break
        except:
            print("ERROR: Closing port")
        ser.close()
    return esn_list

if __name__ == '__main__':
    ports = list_usable_USB()
    list = list_esn(ports)



    print("")

