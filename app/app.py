#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:52:19 2018

http://biobits.org/bokeh-flask.html

@author: Laurent Rudloff
"""

from modules.spectrum import Spectrum_reader
specreader = Spectrum_reader()

#from modules.victor import Victor
#victor=Victor()

from flask import Flask, render_template, request

from flask_dropzone import Dropzone
import os

from bokeh.embed import components



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    #DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=3,
    DROPZONE_UPLOAD_ON_CLICK=True,
    )

dropzone = Dropzone(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    
    feature_names = 'peas'
    
    plot=specreader.get_plot()
    script, div = components(plot)
    return render_template('index.html',
                           script=script,
                           div=div,
                           feature_names=feature_names,
                           )



if __name__ == '__main__':
    app.run(debug=True)