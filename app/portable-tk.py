#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  18 14:52:19 2018
@author: Laurent Rudloff
"""

__author__ = 'Larry'

import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import sys
from tkinter import messagebox

import time

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


from modules.victor import Victor
victor=Victor()

from modules.database_mng import Databasemng
databasemng = Databasemng()


class Homepage:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x480")
        self.master.resizable(width=False, height=False)


        self.customFont = tkFont.Font(family="Helvetica", size=36, weight='bold')

        self.peviousimg = Image.open('img/previous.png')
        self.peviousimg = self.peviousimg.resize((60, 60))
        self.peviousico = ImageTk.PhotoImage(self.peviousimg)

        self.logoimg = Image.open('img/bulb.png')
        self.logoimg = self.logoimg.resize((30, 30))
        self.logoico = ImageTk.PhotoImage(self.logoimg)

        self.master.title('homepage')
        self.mainwindow = tk.Frame(self.master) #, bg='red'
        self.mainwindow.pack(fill=tk.BOTH, expand=1)

        #Logo
        self.logo = tk.Label(self.mainwindow,
                                 text="Smart NIR",
                                 image=self.logoico,
                                 compound=tk.LEFT,
                                 font=self.customFont,)

        #Previous buttom
        self.previous = tk.Button(self.mainwindow,
                                  image=self.peviousico,
                                  text=time.strftime('%d/%m/%Y %H:%M:%S'),
                                  #background='red',
                                  compound=tk.LEFT,
                                  command=self.createhomepage)

        self.createhomepage()

    def cleanframe(self):
        #print(self.mainwindow.grid_size())

        #Grid reset
        for x in range(self.mainwindow.grid_size()[1]):
            self.mainwindow.rowconfigure(x, weight=0)

        for x in range(self.mainwindow.grid_size()[0]):
            self.mainwindow.columnconfigure(x, weight=0)


        for widget in self.mainwindow.winfo_children():
            widget.grid_remove()
            widget.grid_forget()

        # Date update
        self.previous.config(text=time.strftime('%d/%m/%Y %H:%M:%S'))

    def createhomepage(self):
        self.master.title('homepage')
        self.cleanframe()

        #Predict button
        predict = tk.Button(self.mainwindow,
                             text="Predict",
                             command=self.createpredictpage,
                             font=self.customFont)

        #Info button
        about = tk.Button(self.mainwindow,
                          text="About",
                          command=self.createabout,
                          font=self.customFont)

        #display log button
        logspec = tk.Button(self.mainwindow,
                             text="Log",
                             command=self.show_log,
                             font=self.customFont)

        #Admin button
        admin = tk.Button(self.mainwindow,
                            text="Admin",
                            command=self.createadmin,
                            font=self.customFont)

        #self.quitting button
        quit = tk.Button(self.mainwindow,
                          text ="Quit",
                          command = self.quit,
                          font=self.customFont)

        #Logo
        self.logo.grid(row=0, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        self.mainwindow.rowconfigure(0, weight=1, uniform='a')

        #Predict button
        predict.grid(row=1, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        self.mainwindow.rowconfigure(1, weight=1, uniform='a')

        #Info button
        about.grid(row=4, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        self.mainwindow.rowconfigure(2, weight=1, uniform='a')

        #display log button
        logspec.grid(row=2, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        self.mainwindow.rowconfigure(3, weight=1, uniform='a')

        #Admin button
        admin.grid(row=3, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        self.mainwindow.rowconfigure(4, weight=1, uniform='a')

        #self.quitting button
        quit.grid(row=5, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        self.mainwindow.rowconfigure(5, weight=1, uniform='a')

        #Window stretch
        self.mainwindow.columnconfigure(0, weight=1)
        #print(self.mainwindow.grid_size())

    def createpredictpage(self, prediction=None, performance={1:.6, 2:.8}, canvas=None, df=pd.DataFrame(), allowrecord=True):
        self.master.title('Prediction')
        self.cleanframe()

        #extra button creation
        predicted = tk.Label(self.mainwindow,
                         font=self.customFont,)
        if prediction == None:
            predicted.config(text='-')
        else:
            predicted.config(text='{:.2f}'.format(prediction))

        predictaction = tk.Button(self.mainwindow,
                                  text="Predict",
                                  command=self.predictspectra,
                                  font=self.customFont)
        if allowrecord:
            record = tk.Button(self.mainwindow,
                                text="Record entry",
                                command = lambda : messagebox.showerror("Error", "No spectra") if df.shape[0] == 0 else self.record_entry(df),
                                font=self.customFont)
            record.grid(column=0, row=2, columnspan=2, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)

        rmsecvlabel = tk.Label(self.mainwindow,
                               font=self.customFont)
        if victor.trained:
            rmsecvlabel.config(text='{:.2f}'.format(victor.rmsecv))
        else:
            rmsecvlabel.config(text='Not trained')

        #Window creation
        self.previous.grid(column=0, row=0, columnspan=2, sticky=(tk.N,tk.S,tk.W), pady=5, padx=5)

        predictaction.grid(column=2, row=2, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        predicted.grid(column=0, row=1, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        rmsecvlabel.grid(column=1, row=1, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)


        self.mainwindow.rowconfigure(0, weight=1, uniform='b')
        self.mainwindow.rowconfigure(1, weight=2, uniform='b')
        self.mainwindow.rowconfigure(2, weight=1, uniform='b')

        self.mainwindow.columnconfigure(0, weight=1)
        self.mainwindow.columnconfigure(1, weight=1)
        self.mainwindow.columnconfigure(2, weight=4)

        if canvas==None:
            waitingimg = Image.open('img/waiting.png')
            waitingimg = waitingimg.resize((30, 30))
            waitingico = ImageTk.PhotoImage(waitingimg)

            waiting = tk.Label(self.mainwindow,
                               text='in progress',
                               image = waitingico,
                               compound=tk.TOP)
            waiting.grid(column=2, row=0, rowspan=2, sticky=(tk.N,tk.S,tk.W,tk.E))
        else:
            canvas.get_tk_widget().grid(column=2, row=0, rowspan=2, sticky=(tk.N,tk.S,tk.W,tk.E))

    def quit(self):
        """Quit the apps, save the temp data"""
        print('by by !!')
        self.master.quit()
        sys.exit()

    def predictspectra(self):
        if victor.trained:
            index = np.random.random_integers(databasemng.get_db(shape=True))
            df = databasemng.get_db().iloc[[index]]
            self.createpredictpage(prediction=victor.predict(df)[0], canvas=self.get_plot(df), df=df)
        else:
            messagebox.showerror("Error", "Model no trained")

    def get_plot(self, dataset=None):
        f = Figure(figsize=(4, 3), dpi=100)
        a = f.add_subplot(111)
        df = dataset[['wl_{}'.format(x) for x in range(950, 1530+1, 2)]]

        x = [int(x.split('_')[1]) for x in df.columns]
        y = df.iloc[0]
        #x = np.arange(0.0, 3.0, 0.01)
        #y = np.sin(2*np.pi*t)

        a.plot(x, y)
        #a.set_title('Tk embedding')
        a.set_xlabel('Wave length')
        a.set_ylabel('Intensity')


        # a tk.DrawingArea
        canvas = FigureCanvasTkAgg(f, master=self.mainwindow)
        return canvas

    def record_entry(self, df):
        messagebox.showinfo("Confirmation", "Entry saved")

    def show_log(self, entryrange=4, start=0):
        self.master.title('Log')
        self.cleanframe()
        self.previous.grid(column=0, row=0, sticky=(tk.N,tk.S,tk.W), pady=5, padx=5)

        df = databasemng.get_db().iloc[start:start+entryrange]
        button=[]
        index=0
        for _, line in df.iterrows():
            button.append(tk.Button(self.mainwindow,
                                    text=line['time'],
                                    command=lambda index=index: self.createpredictpage(prediction=victor.predict(df)[index], canvas=self.get_plot(df.iloc[[index]]), df=df.iloc[[index]], allowrecord=False),
                                    font=self.customFont))
            button[index].grid(row=index+1, columnspan=2, sticky=(tk.N,tk.S,tk.W,tk.E))
            index+=1
        self.mainwindow.columnconfigure(0, weight=1)

        pagenum = tk.Label(self.mainwindow, text='{}/{}'.format(start//entryrange+1, databasemng.get_db().shape[0]//entryrange), font=self.customFont)
        pagenum.grid(column=1, row=0, sticky=(tk.N,tk.S,tk.W), pady=5, padx=5)
        self.mainwindow.columnconfigure(1, weight=3)

        navbuttons = tk.Frame(self.mainwindow)
        navbuttons.grid(row=entryrange+1, columnspan=2, sticky=(tk.N,tk.S,tk.W,tk.E), pady=3, padx=3)

        plus = tk.Button(navbuttons, text='+', font=self.customFont,
                         command = lambda : self.show_log(start = start+entryrange+1))
        plus.grid(column=1, row=0, sticky=(tk.N,tk.S,tk.W,tk.E), pady=3, padx=3)
        minus = tk.Button(navbuttons, text='-', font=self.customFont,
                         command = lambda : self.show_log(start = start-entryrange+1))
        minus.grid(column=0, row=0, sticky=(tk.N,tk.S,tk.W,tk.E), pady=3, padx=3)

        navbuttons.columnconfigure(0, weight=1, uniform='a')
        navbuttons.columnconfigure(1, weight=1, uniform='a')
        navbuttons.rowconfigure(0, weight=1)

    def createadmin(self):
        messagebox.showinfo("Info", "Work in progress")

    def createabout(self):
        self.master.title('About')
        self.cleanframe()

        version = tk.Label(self.mainwindow, text='0.0 beta', font=self.customFont,)
        poweredby = tk.Label(self.mainwindow, text='Powered by: Python, Tkinter, sklearn, Numpy, Matplotlib, Pandas, SPC...',)
        softname = tk.Label(self.mainwindow, text='NIR touch', font=self.customFont,)
        #bycompany = tk.Label(self.mainwindow, text='by smart', font=self.customFont,)

        #Window creation
        self.previous.grid(row=0, sticky=(tk.N,tk.S,tk.W), pady=5, padx=5)
        softname.grid(row=1, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        version.grid(row=2, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        poweredby.grid(row=3, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)

        #print(self.mainwindow.grid_size())
        for x in range(self.mainwindow.grid_size()[1]):
            self.mainwindow.rowconfigure(x, weight=1, uniform='c')
        self.mainwindow.columnconfigure(0, weight=1)






if __name__ == '__main__':
    root = tk.Tk()
    app = Homepage(root)
    root.mainloop()
