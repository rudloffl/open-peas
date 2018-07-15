#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:11:04 2018

@author: Laurent Rudloff
"""

import numpy as np
import pandas as pd

from bokeh.plotting import figure, output_file, show
import matplotlib.pyplot as plt



class Plot_tool():
    def __init__(self):
        """"""
        pass

    def get_spectrums(self, df):
        x = df.columns
        y = df.iloc[0]


        TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,hover"

        # create a new plot with a title and axis labels
        p = figure(title="Spectrogram sample",
                   x_axis_label='x',
                   y_axis_label='y',
                   tools=TOOLS,
                   )

        # add a line renderer with legend and line thickness
        p.line(x, y,
               legend="wave length",
               line_width=3,
               line_color='seagreen',
               line_join='bevel',
               name='green peas')

        # show the results
        return p

if __name__ == '__main__':
    plot_tool = Plot_tool()
    show(plot_tool.get_plot())
