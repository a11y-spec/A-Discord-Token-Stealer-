import pymem
import subprocess


try:
    mem = pymem.Pymem("cmd.exe") ### reads memory of notepad.exe
except:
    subprocess.Popen("cmd.exe")
    mem = pymem.Pymem("cmd.exe")

mem.inject_python_interpreter() 


code = """ 

import tkinter as tk
win = tk.Tk()



win.mainloop()




"""

mem.inject_python_shellcode(code) 