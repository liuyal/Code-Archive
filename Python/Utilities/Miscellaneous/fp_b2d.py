import os, sys, math

# https://www.exploringbinary.com/binary-converter/
# https://www.asciitohex.com/

def binary2float(bin):
    item = bin
    b_list = list(item)
    b_list.pop(0)
    power = -1
    float_number = 0.00
    for char in b_list:
        x = 0.00
        if char == "1":
            x = 2.0 ** (power)
        else:
            x = 0.00
        power = power - 1
        float_number = float_number + x
    return float_number


def binaryGen():
    inc = 0b00000000000000000000000000000001
    x = 0b00000000000000000000000000000000
    for i in range(0, 1000):
        print(format(x, '#034b'))
        x = x + inc


def calc_vec_results():
    input = open("vectors.txt", "r").readlines()
    output = open("results.txt", "r").readlines()
    input_dec = []
    output_dec = []
    input_hex = []
    output_hex = []
    for item in input:
        input_dec.append(binary2float(item.replace('\n', '')))
        input_hex.append(hex(int(item.replace('\n', ''), 2)))
    for item in output:
        output_dec.append(binary2float(item.replace('\n', '')))
        output_hex.append(hex(int(item.replace('\n', ''), 2)))

    w_file = open(os.getcwd() + os.sep + "b2d.csv", "a+")
    w_file.truncate(0)
    w_file.write("input (BIN),input (HEX),input (DEC),output (BIN),output (HEX),output (DEC)\n")
    for i in range(0, len(input)):
        line = input[i].replace('\n', '') + "," + input_hex[i].replace("0x","").upper() + "," + str(input_dec[i]) + "," + output[i].replace('\n', '') + "," + output_hex[i].replace("0x","").upper() + "," + str(output_dec[i])
        w_file.write(line + "\n")
        print(line)
    w_file.flush()
    w_file.close()

    input_dec = list(dict.fromkeys(input_dec))
    output_dec = list(dict.fromkeys(output_dec))
    input_hex = list(dict.fromkeys(input_hex))
    output_hex = list(dict.fromkeys(output_hex))

    w_file = open(os.getcwd() + os.sep + "b2d_no_repeat.csv", "a+")
    w_file.truncate(0)
    w_file.write("input (BIN),input (HEX),input (DEC),output (BIN),output (HEX),output (DEC)\n")
    for i in range(0, len(input_dec)):
        line = input[i].replace('\n', '') + "," + input_hex[i].replace("0x", "").upper() + "," + str(input_dec[i]) + "," + output[i].replace('\n', '') + "," + output_hex[i].replace("0x", "").upper() + "," + str(output_dec[i])
        w_file.write(line + "\n")
        print(line)
    w_file.flush()
    w_file.close()


def gen_testcase():
    n = 5000
    input = open("vectors.txt", "r").readlines()
    input_hex = []
    input_bin = []
    for item in input: input_hex.append(hex(int(item.replace('\n', ''), 2)).replace("0x",""))
    for item in input: input_bin.append(item.replace("\n",""))

    input_hex = list(dict.fromkeys(input_hex))
    input_bin = list(dict.fromkeys(input_bin))

    line = '''\t\tEXT_MR <= '0'; EXT_MW <= '1'; EXT_ADDRBUS <= X"zzzzzzzz"; EXT_WDATABUS <= X"xxxxxxxx"; wait for clock_period; --'''
    input_vhdl = []
    addr = int("40001000", 16)
    for i in range(0, n):
        if i >= len(input_hex): break
        hex_addr = hex(addr).replace("0x","")
        new_line = line.replace("zzzzzzzz", hex_addr).replace("xxxxxxxx", input_hex[i]) + str(i+1)
        input_vhdl.append(new_line)
        addr += 1

    w_file1 = open(os.getcwd() + os.sep + "input_vhdl.txt", "a+")
    w_file2 = open(os.getcwd() + os.sep + "input_hex.txt", "a+")
    w_file3 = open(os.getcwd() + os.sep + "input_bin.txt", "a+")
    w_file1.truncate(0); w_file2.truncate(0); w_file3.truncate(0)
    for i in range(0, n):
        if i >= len(input_hex): break
        w_file1.write(input_vhdl[i] + "\n")
        w_file2.write(input_hex[i] + "\n")
        w_file3.write(input_bin[i] + "\n")
    w_file1.flush(); w_file2.flush(); w_file3.flush()
    w_file1.close(); w_file2.close(); w_file3.close()

if __name__ == "__main__":
    # binaryGen()
    calc_vec_results()
    gen_testcase()