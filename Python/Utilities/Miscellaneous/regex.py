import re

text = 'root@ND888888888:~#\r'
found = ""
m = re.search('@(.+?):', text)
if m: found = m.group(1)

print(found)