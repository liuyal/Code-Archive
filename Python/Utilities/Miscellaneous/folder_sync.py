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


def sync_callback():
    source_path = text_src.get("1.0", 'end-1c')
    target_path = text_dst.get("1.0", 'end-1c')
    sync(source_path, target_path, 'sync')


def browse_src_button():
    filename = fd.askdirectory()
    text_src.delete("1.0", "end")
    text_src.insert(tk.END, filename)


def browse_dst_button():
    filename = fd.askdirectory()
    text_dst.delete("1.0", "end")
    text_dst.insert(tk.END, filename)


if __name__ == "__main__":
    root = tk.Tk(className='Folder Sync')
    root.resizable(width=False, height=False)
    root.geometry("640x140")

    root.grid_rowconfigure(0, minsize=20)

    label_src = tk.Label(master=root, width=10, anchor="e", text="Source")
    label_src.grid(row=1, column=1)
    label_dst = tk.Label(master=root, width=10, anchor="e", text="Destination")
    label_dst.grid(row=2, column=1)

    text_src = tk.Text(root, height=1, width=54)
    text_src.grid(row=1, column=2)
    text_src.insert(tk.END, "")
    text_dst = tk.Text(root, height=1, width=54)
    text_dst.grid(row=2, column=2)
    text_dst.insert(tk.END, "")

    button_src = Button(text="Browse", width=15, command=browse_src_button)
    button_src.grid(row=1, column=3)
    button_src = Button(text="Browse", width=15, command=browse_dst_button)
    button_src.grid(row=2, column=3)

    root.grid_rowconfigure(3, minsize=30)

    f = tk.Frame(root)
    f.grid(row=4, column=3, sticky=tk.SE)

    btn_quit = tk.Button(f, width=6, text='Exit', command=root.destroy)
    btn_quit.pack(side=RIGHT, padx=5, pady=5)

    btn_sync = tk.Button(f, width=6, text='Sync', command=sync_callback)
    btn_sync.pack(side=RIGHT)

    root.mainloop()
