#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:52:19 2018

http://biobits.org/bokeh-flask.html

@author: Laurent Rudloff
"""

__author__ = 'Larry'

from modules.spectrum import Spectrum_reader
specreader = Spectrum_reader()

#from modules.victor import Victor
#victor=Victor()

from modules.plot_tool import Plot_tool
plot_tool = Plot_tool()

from modules.database_mng import Databasemng
databasemng = Databasemng()



from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

import os

from bokeh.embed import components


app = Flask(__name__)
app.config['SECRET_KEY'] = "12345"

basedir = os.path.abspath(os.path.dirname(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/result", methods=['POST'])
def upload():
    #print(request.files.getlist("predict"))

    if len(request.files.getlist("predict")) == 0:
        return 'Nofile'

    spectras = specreader.load_files(request.files.getlist("predict"))

    plot=plot_tool.get_spectrums(spectras)
    script, div = components(plot)
    feature_names = 'peas'
    return render_template('result.html',
                           script=script,
                           div=div,
                           feature_names=feature_names,
                      )

@app.route("/constructset", methods=['POST'])
def construct():
    if len(request.files.getlist("spectrumset")) == 0:
        return 'Please upload spectrums'
    if len(request.files.getlist("target")) == 0:
        return 'Please upload targets'

    spectras = specreader.load_files(request.files.getlist("spectrumset"))
    targets = databasemng.read_targets(request.files.getlist("target")[0])

    databasemng.createdb(spectras, targets)
    return 'in progress'

@app.route("/showdb", methods=['POST'])
def showdb():
    return 'to do !'

if __name__ == '__main__':
    app.run(debug=True)
