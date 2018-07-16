#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  15 14:52:19 2018
@author: Laurent Rudloff
"""

__author__ = 'Larry'

import numpy as np
import pandas as pd
from io import StringIO
import os

#where are we ?
basedir = os.path.abspath(os.path.dirname(__file__))

class Databasemng():
    """pandas version, sqlite to come"""
    def __init__(self, bcupath = 'backup'):
        self.columns = []
        self.columns.extend(['time'])
        self.columns.extend(['customerID', 'customer'])
        self.columns.extend(['temperature',])
        self.columns.extend(['long', 'lat'])
        self.columns.extend(['vegetable', 'sampleID'])
        self.columns.extend([int(x) for x in range(950, 1530+1, 2)])
        self.columns.append('target')

        self.dataset = pd.DataFrame(columns = self.columns)

        subfolder = basedir.split('/')[:-1]
        self.bcupath = os.path.join('/', *subfolder, bcupath, 'dataset.csv')

        self.temppath = os.path.join('/', *subfolder, bcupath, 'temp.spc')

    def createdb(self, df, targets):
        sampleid = 0
        self.dataset = pd.DataFrame(columns=self.columns)
        for index, line in df.iterrows():
            line = line.to_frame().T

            details = {}

            # Target
            details['target'] = targets.Average.iloc[index]

            # sample ID
            if sampleid == 0 and index ==0:
                sampleid = 0
            elif index != 0 and details['target'] != targets['Average'].iloc[index-1]:
                sampleid += 1
            else:
                pass #same subsample

            details['sampleID'] = sampleid

            #Additionnal data
            misc = pd.DataFrame(details, index=[1])

            line = pd.concat([misc, line], axis=1)

            self.dataset = self.dataset.append(line, ignore_index=True)

        self.savedb()

    def adddb(self, df):
        pass

    def get_db(self):
        pass

    def savedb(self):
        self.dataset.to_csv(self.bcupath)

    def loaddb(self):
        pass

    def read_targets(self, filestream):
        """Reads and returns the excel target set"""
        subfolder = basedir.split('/')[:-1]
        temppath = os.path.join('/', *subfolder, 'backup', 'targets.xlsx')
        filestream.save(temppath)
        targets = pd.read_excel(temppath)
        print('Yayyy')
        return targets
