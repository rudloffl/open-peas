#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:11:04 2018

@author: Laurent Rudloff
"""

import numpy as np
import pandas as pd
import spc
from io import StringIO
import os

#where are we ?
basedir = os.path.abspath(os.path.dirname(__file__))

class Spectrum_reader():
    def __init__(self, bcupath='backup'):
        """"""
        self.bcupath = bcupath

    def load_files(self, filestream):
        """loads the spc file and returns a pandas dataframe"""

        columns = []
        columns.extend([int(x) for x in range(950, 1530+1, 2)])
        dataset = pd.DataFrame(columns=columns)

        for file in filestream:
            details = {}
            filename = file.filename

            # Timestamp
            timestamp = '-'.join(filename.split('_')[:2])
            time = pd.to_datetime(timestamp, format='%Y%m%d-%H%M%S')
            details['time'] = time

            subfolder = basedir.split('/')[:-1]
            temppath = os.path.join('/', *subfolder, self.bcupath, 'temp.spc')
            #print(basedir)
            #print(temppath)
            file.save(temppath)

            f = spc.File(temppath)
            data = f.data_txt(delimiter=';', newline='\n')
            spectra = StringIO(data)
            df = pd.read_csv(spectra, sep=";", header=None, dtype={0:'int', 1:'float64'})
            df.set_index(0, inplace=True)
            df = df.T

            # Additionnal information
            misc = pd.DataFrame(details, index=[1])
            df = pd.concat([df, misc], axis =1)

            # Merging to the dataset to return
            dataset = dataset.append(df, ignore_index=True)

        #print(dataset.shape)

        return dataset



    def get_plot_sample(self):
        # prepare some data
        x = np.linspace(-5,5,200)
        y = x**2


        TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,hover"

        # create a new plot with a title and axis labels
        p = figure(title="A really odd Spectrogram",
                   x_axis_label='x',
                   y_axis_label='y',
                   tools=TOOLS,
                   )

        # add a line renderer with legend and line thickness
        p.line(x, y,
               legend="Squared Func.",
               line_width=3,
               line_color='seagreen',
               line_join='bevel',
               name='green peas')

        # show the results
        return p

if __name__ == '__main__':
    specreader = Spectrum_reader()
    show(specreader.load_files())
