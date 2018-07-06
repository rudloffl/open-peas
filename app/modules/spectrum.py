#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:11:04 2018

@author: Laurent Rudloff
"""

import numpy as np
#import pandas as pd

from bokeh.plotting import figure, output_file, show

class Spectrum_reader():
    def __init__(self):
        """"""
        pass
    
    def load_file(self):
        """loads the spc file"""
        pass
    
    def get_plot(self):
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
    show(specreader.get_plot())