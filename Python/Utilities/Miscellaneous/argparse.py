import argparse, sys

parser = argparse.ArgumentParser(description='', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-a', "--run", dest="auto_run", action='store_true', default=True, help='Automatically run synthesiser with dc_shell [DEFAULT]')
parser.add_argument('-c', "--combine", dest="path", action='store', help='Combine auto_results in folder: <PATH>')
parser.add_argument('-p', "--parse", dest="hspice_file", action='store', help='Parse Hspice output file at: <PATH>')
parser.add_argument('-d', "--debug", dest="debug", action='store_true', default=False, help='Debug Mode')
input_arg = parser.parse_args()
try:
    sys.argv[1]
except:
    parser.print_help()

print(input_arg)