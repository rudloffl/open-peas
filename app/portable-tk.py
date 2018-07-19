#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  18 14:52:19 2018
@author: Laurent Rudloff
"""

__author__ = 'Larry'

from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Smart NIR")
root.resizable(width=False, height=False)
root.geometry("800x480")

s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 48, 'bold', 'italic'))

root.columnconfigure(0, weight=1)


def helloCallBack():
   print('Yayyy!')

predict = ttk.Button(root, text ="Predict", command = helloCallBack, style='my.TButton')
predict.grid(column=0, row=0, sticky=(N,S,W,E), pady=5, padx=5)
root.rowconfigure(0, weight=1, uniform='a')


info = ttk.Button(root, text ="Info", command = helloCallBack, style='my.TButton')
info.grid(column=0, row=1, sticky=(N,S,W,E), pady=5, padx=5)
root.rowconfigure(1, weight=1, uniform='a')


logspec = ttk.Button(root, text ="Log", command = helloCallBack, style='my.TButton')
logspec.grid(column=0, row=2, sticky=(N,S,W,E), pady=5, padx=5)
root.rowconfigure(2, weight=1, uniform='a')


calibration = ttk.Button(root, text ="Calibration", command = helloCallBack, style='my.TButton')
calibration.grid(column=0, row=3, sticky=(N,S,W,E), pady=5, padx=5)
root.rowconfigure(3, weight=1, uniform='a')



def quit():
    """Quit the apps, save the temp data"""
    global root
    root.quit()

quit = ttk.Button(root, text ="Quit", command = quit, style='my.TButton')
quit.grid(column=0, row=4, sticky=(N,S,W,E), pady=5, padx=5)
root.rowconfigure(4, weight=1, uniform='a')


#d=StatusBar(root)
root.mainloop()
