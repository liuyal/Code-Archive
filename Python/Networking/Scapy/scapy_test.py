from scapy.all import *

A = "192.168.1.99" # spoofed source IP address
B = "192.168.1.103" # destination IP address
C = 9996 # source port
D = 9996 # destination port
payload = "yada yada yada" # packet payload

while True:
    spoofed_packet = IP(src=A, dst=B) / UDP(sport=C, dport=D) / payload
    send(spoofed_packet)
    time.sleep(1)