import os
import sys
import time
import shutil
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style
from dirsync import sync


def callback():
    sync(source_path, target_path, 'sync')
    # print(fd.askopenfilename())

if __name__ == "__main__":

    target_path = r"C:\Users\Jerry\Desktop\test\dst"
    source_path = r"C:\Users\Jerry\Desktop\test\src"

    gui = tk.Tk(className='Folder Sync')
    gui.geometry("500x200")

    frame = Frame(gui, relief=RAISED, borderwidth=1)
    frame.pack(fill=BOTH, expand=True)

    btn_sync = tk.Button(text='Sync', command=callback)
    btn_quit = tk.Button(text='Exit', command=gui.destroy)
    btn_quit.pack(side=RIGHT, padx=5, pady=5)
    btn_sync.pack(side=RIGHT)

    gui.mainloop()

