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

        peviousimg = Image.open('img/previous.png')
        peviousimg = peviousimg.resize((60, 60))
        self.peviousico = ImageTk.PhotoImage(peviousimg)

        logoimg = Image.open('img/logo.png')
        logoimg = logoimg.resize((277, 80))
        self.logoico = ImageTk.PhotoImage(logoimg)

        self.master.title('homepage')
        self.mainwindow = tk.Frame(self.master) #, bg='red'
        self.mainwindow.pack(fill=tk.BOTH, expand=1)

        #Logo
        self.logo = tk.Label(self.mainwindow,
                                 #text="Smart NIR",
                                 image=self.logoico,
                                 #compound=tk.LEFT,
                                 font=self.customFont,)

        #Previous buttom
        self.previous = tk.Button(self.mainwindow,
                                  image=self.peviousico,
                                  #text=time.strftime('%d/%m/%Y %H:%M:%S'),
                                  #background='red',
                                  #compound=tk.LEFT,
                                  command=self.createhomepage)

        self.createhomepage()

    def cleanframe(self):
        #print('before', self.mainwindow.grid_size())

        for widget in self.mainwindow.winfo_children():
            widget.grid_remove()
            widget.grid_forget()

        #Grid reset
        for x in range(self.mainwindow.grid_size()[1]):
            self.mainwindow.rowconfigure(x, weight=0, minsize=0, pad=0)

        for x in range(self.mainwindow.grid_size()[0]):
            self.mainwindow.columnconfigure(x, weight=0, minsize=0, pad=0)

        #print('after', self.mainwindow.grid_size())
        self.mainwindow.grid_bbox(column=0, row=0, col2=0, row2=0)
        # Date update
        #self.previous.config(text=time.strftime('%d/%m/%Y %H:%M:%S'))

    def createhomepage(self):
        self.master.title('homepage')
        self.cleanframe()

        pictosize=(80,80)

        #Predict button
        predictimg = Image.open('img/predict.png')
        predictimg = predictimg.resize(pictosize)
        self.predictico = ImageTk.PhotoImage(predictimg)
        predict = tk.Button(self.mainwindow,
                             text="   Predict",
                             image=self.predictico,
                             compound=tk.LEFT,
                             command=self.createpredictpage,
                             font=self.customFont,
                             anchor='w',
                             padx=5,
                             )

        #Info button
        aboutimg = Image.open('img/about.png')
        aboutimg = aboutimg.resize(pictosize)
        self.aboutico = ImageTk.PhotoImage(aboutimg)
        about = tk.Button(self.mainwindow,
                          text="   About",
                          image=self.aboutico,
                          compound=tk.LEFT,
                          command=self.createabout,
                          font=self.customFont,
                          anchor='w',
                          padx=5,
                          )

        #display log button
        logimg = Image.open('img/log.png')
        logimg = logimg.resize(pictosize)
        self.logico = ImageTk.PhotoImage(logimg)
        logspec = tk.Button(self.mainwindow,
                             text="   Log",
                             image=self.logico,
                             compound=tk.LEFT,
                             command=self.show_log,
                             font=self.customFont,
                             anchor='w',
                             padx=5,)

        #Admin button
        adminimg = Image.open('img/admin.png')
        adminimg = adminimg.resize(pictosize)
        self.adminico = ImageTk.PhotoImage(adminimg)
        admin = tk.Button(self.mainwindow,
                            text="   Admin",
                            command=self.createadmin,
                            font=self.customFont,
                            image=self.adminico,
                            compound=tk.LEFT,
                            anchor='w',
                            padx=5,)

        #self.quitting button
        quitimg = Image.open('img/quit.png')
        quitimg = quitimg.resize(pictosize)
        self.quitico = ImageTk.PhotoImage(quitimg)
        quit = tk.Button(self.mainwindow,
                          text ="   Quit",
                          command = self.quit,
                          font=self.customFont,
                          image=self.quitico,
                          compound=tk.LEFT,
                          anchor='w',
                          padx=5,)

        #Logo
        self.logo.grid(row=0, columnspan=2, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)

        #Predict button
        predict.grid(row=1, column=0, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)

        #Info button
        about.grid(row=2, column=1, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)

        #display log button
        logspec.grid(row=1, column=1, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)

        #Admin button
        admin.grid(row=2, column=0, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)

        #self.quitting button
        quit.grid(row=3, column=0, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)

        #Window stretch
        for x in range(3+1):
            self.mainwindow.rowconfigure(x, weight=1, uniform='a')

        self.mainwindow.columnconfigure(0, weight=1, uniform='b')
        self.mainwindow.columnconfigure(1, weight=1, uniform='b')
        #print(self.mainwindow.grid_size())

    def createpredictpage(self, prediction=None, performance=[(1,33), (3,66)], canvas=None, df=pd.DataFrame(), allowrecord=True):
        self.master.title('Prediction')
        self.cleanframe()

        #Result Drawing
        result = tk.Frame(self.mainwindow,
                          background='grey70',
                          borderwidth=4,
                          relief='raised')
        acc1 = tk.Label(result,background='grey70',
                        text='+/- {} -> {}%'.format(performance[0][0], performance[0][1]))
        acc2 = tk.Label(result,background='grey70',
                        text='+/- {} -> {}%'.format(performance[1][0], performance[1][1]))

        predicted = tk.Label(result, font=self.customFont,background='grey70',)

        if prediction == None:
            predicted.config(text='-')
        else:
            predicted.config(text='{:.2f}'.format(prediction))

        predicted.grid(column=0, row=0, rowspan=2, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        acc1.grid(column=1, row=0, sticky=(tk.S,tk.W,tk.E), pady=5, padx=5)
        acc2.grid(column=1, row=1, sticky=(tk.N,tk.W,tk.E), pady=5, padx=5)
        result.columnconfigure(0, weight=1, uniform='d')
        result.columnconfigure(1, weight=1, uniform='d')
        result.rowconfigure(1, weight=1, uniform='e')
        result.rowconfigure(0, weight=1, uniform='e')

        predictimg = Image.open('img/predict.png')
        predictimg = predictimg.resize((60,60))
        self.predictico = ImageTk.PhotoImage(predictimg)
        predictaction = tk.Button(self.mainwindow,
                                  text="   Predict",
                                  command=self.predictspectra,
                                  font=self.customFont,
                                  image=self.predictico,
                                  compound=tk.LEFT,
                                  #anchor='w',
                                  padx=5,)
        if allowrecord:
            recordimg = Image.open('img/record.png')
            recordimg = recordimg.resize((60,60))
            self.recordico = ImageTk.PhotoImage(recordimg)
            record = tk.Button(self.mainwindow,
                                text=" Record entry",
                                command = lambda : messagebox.showerror("Error", "No spectra") if df.shape[0] == 0 else self.record_entry(df),
                                font=self.customFont,
                                image=self.recordico,
                                compound=tk.LEFT,
                                padx=5)
            record.grid(column=0, row=2, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)


        #if victor.trained:
        #    rmsecvlabel.config(text='{:.2f}'.format(victor.rmsecv))
        #else:
        #    rmsecvlabel.config(text='Not trained')

        #Window creation
        self.previous.grid(column=0, row=0, sticky=(tk.N,tk.S,tk.W), pady=5, padx=5)
        predictaction.grid(column=1, row=2, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        result.grid(column=0, row=1, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)

        #rmsecvlabel = tk.Label(self.mainwindow, font=self.customFont)
        #rmsecvlabel.grid(column=1, row=1, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)


        self.mainwindow.rowconfigure(0, weight=1, uniform='b')
        self.mainwindow.rowconfigure(1, weight=2, uniform='b')
        self.mainwindow.rowconfigure(2, weight=1, uniform='b')

        self.mainwindow.columnconfigure(0, weight=2)
        self.mainwindow.columnconfigure(1, weight=3)

        if canvas==None:
            waitingimg = Image.open('img/waiting.png')
            waitingimg = waitingimg.resize((150, 150))
            self.waitingico = ImageTk.PhotoImage(waitingimg)

            waiting = tk.Label(self.mainwindow,
                               #text='in progress',
                               image = self.waitingico,
                               )
            waiting.grid(column=1, row=0, rowspan=2, sticky=(tk.N,tk.S,tk.W,tk.E))
        else:
            canvas.get_tk_widget().grid(column=1, row=0, rowspan=2, sticky=(tk.N,tk.S,tk.W,tk.E), ipadx=20, ipady=20)

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
        a.set_title('Spectrum')


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
        softname = tk.Label(self.mainwindow, text='NIRS touch', font=self.customFont,)
        #bycompany = tk.Label(self.mainwindow, text='by smart', font=self.customFont,)

        #Window creation
        self.previous.grid(row=0, column=0, sticky=(tk.N,tk.S,tk.W), pady=5, padx=5)
        softname.grid(row=1, column=0, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        version.grid(row=2, column=0, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)
        poweredby.grid(row=3, column=0, sticky=(tk.N,tk.S,tk.W,tk.E), pady=5, padx=5)

        #print(self.mainwindow.grid_size())
        for x in range(self.mainwindow.grid_size()[1]):
            self.mainwindow.rowconfigure(x, weight=1, uniform='c')

        self.mainwindow.columnconfigure(0, weight=1)






if __name__ == '__main__':
    root = tk.Tk()
    app = Homepage(root)
    root.mainloop()
