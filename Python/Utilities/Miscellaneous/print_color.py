
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(f"{bcolors.WARNING}Warning: No active frommets remain. Continue?{bcolors.ENDC}")

# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences

def print_custom(msg="", color="White", mod=[], custom=False, rgb=[0,0,0]):
    if custom:
        r = str(rgb[0])
        g = str(rgb[1])
        b = str(rgb[2])
        header = '\033[38;2;' + r + g + b
    print(msg); print(color); print(mod); print(custom); print(rgb)
print_custom(custom=True)

msg = "HELLO WORLD"
for i in range(0, 107):
    print( str(i) + ': ' + "\033[31;"+ str(i) + "m" + msg + "\033[0m")

print ("\033[206m<HOME>\033[0m")
print("\033[31;1;4mHello\033[0m")
print("\033[38;2;23;23;23mRBGGSDG\033[0m")
print('\033[38;2;255;82;197;48;2;155;106;0mHello\033[0m')



