import os

image_path = r"C:\Users\ljerry\Desktop"
build_folder_path = r"//172.16.101.145/DevQA/Image/T11898/R18664_D33327/trunk/"

cmd0 = r'echo from win32com.client import Dispatch > create_shortcut.py'
cmd1 = r"echo shell = Dispatch('WScript.Shell') >> create_shortcut.py"
cmd2 = r'echo shortcut = shell.CreateShortCut("<LOCAL>.lnk") >> create_shortcut.py'
cmd3 = r'echo shortcut.Targetpath = "<LINK>" >> create_shortcut.py'
cmd4 = r'echo shortcut.save() >> create_shortcut.py'
cmd5 = r'python create_shortcut.py'
cmd6 = r'DEL create_shortcut.py /f /q'

cmd_list = [cmd0, cmd1, cmd2, cmd3, cmd4]

item = ' && '.join(cmd_list)
item = item.replace("<LOCAL>", image_path + '\\' + "trunk").replace('\\','\\\\')
item = item.replace("<LINK>", build_folder_path.replace('/', '\\\\'))
print(item.replace(' && ','\n'))
os.system(item)



from win32com.client import Dispatch  
shell = Dispatch('WScript.Shell')  
shortcut = shell.CreateShortCut("C:\\Users\\ljerry\\Desktop\\trunk.lnk")  
shortcut.Targetpath = "\\\\172.16.101.145\\DevQA\\Image\\T11898\\R18664_D33327\\trunk\\"  
shortcut.save() 
