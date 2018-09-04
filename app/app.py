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

from modules.victor import Victor
victor=Victor()

from modules.plot_tool import Plot_tool
plot_tool = Plot_tool()

from modules.database_mng import Databasemng
databasemng = Databasemng()

from modules.sql_manager import Chester
chester = Chester()
chester.createdb()



from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

import os

from bokeh.embed import components


app = Flask(__name__)
app.config['SECRET_KEY'] = "12345"

basedir = os.path.abspath(os.path.dirname(__file__))

@app.route("/")
def index():
    return render_template("home.html",
                            model_trained=victor.trained,
                            rmsecv=victor.rmsecv,
                            datasetsize=databasemng.get_db(shape=True),)

@app.route("/result", methods=['POST'])
def upload():
    if not victor.trained:
        return 'Please train the model first !'

    if len(request.files.getlist("predict")) == 0:
        return 'Nofile'

    spectras = specreader.load_files(request.files.getlist("predict"))

    crushingval = victor.predict(spectras)[0]

    plot=plot_tool.get_spectrums(spectras)
    script, div = components(plot)
    feature_names = 'peas'
    return render_template('result.html',
                           script=script,
                           div=div,
                           feature_names=feature_names,
                           crushingval=crushingval,
                      )

@app.route("/constructset", methods=['POST'])
def construct():
    if len(request.files.getlist("spectrumset")) == 0:
        return 'Please upload spectrums'
    if len(request.files.getlist("target")) == 0:
        return 'Please upload targets'

    targets = databasemng.read_targets(request.files.getlist("target")[0])
    spectras = specreader.load_files(request.files.getlist("spectrumset"))
    databasemng.createdb(spectras, targets)

    victor.fit(databasemng.get_db())
    return 'Congratulation, the model has been trained and is ready to use, RMSECV = {}'.format(victor.rmsecv)

@app.route("/showdb", methods=['POST'])
def showdb():
    return 'to do !'

@app.route("/admin", methods=['POST'])
def admin():
    return render_template('admin.html')

@app.route("/admin_crop", methods=['POST'])
def admin_crop():
    header = chester.get_columns('MATERIAL')
    return render_template('admin_crop.html', header=header,
                                            existing_table=False,
                                            table=[],
                                            existing_cname=[],
                                            existing_supp=[],
                                            existing_variety={},
                                            existing_ref=[])

@app.route("/admin_spectras", methods=['POST'])
def admin_spectras():
    return render_template('admin_spectras.html')

@app.route("/admin_customers", methods=['POST'])
def admin_customers():
    return render_template('admin_customers.html')

@app.route("/admin_conditions", methods=['POST'])
def admin_conditions():

    return render_template('admin_conditions.html')

@app.route("/admin_units", methods=['POST'])
def admin_units():
    return render_template('admin_units.html')

if __name__ == '__main__':
    app.run(debug=True)
