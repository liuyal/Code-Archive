import os, sys, time

stream = open("badData.txt","r+")
list = stream.read().split('\n')
stream.close()

for j in range(0,len(list)):
    item = list[j]

    if "RMC" in item:
        rmc_msg = item.split(',')
        rmc_msg[7] = "1.0"
        new_rmc = ','.join(rmc_msg).split('*')[0].replace('$','')
        i = 0; checksum = 0
        while i < len(new_rmc): checksum ^= ord(new_rmc[i]); i += 1
        hexCheckSum = hex(checksum).rstrip("L").lstrip("0x") or "0"
        final_rmc = '$' + new_rmc + '*' + hexCheckSum.upper()
        list[j] = final_rmc

file = open("newData.txt","w+")
file.truncate(0)
file.write('\n'.join(list))
file.flush()
file.close()
