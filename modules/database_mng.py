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
        self.columns.extend(['wl_{}'.format(x) for x in range(950, 1530+1, 2)])
        self.columns.append('target')



        subfolder = basedir.split('/')[:-1]
        self.bcupath = os.path.join('/', *subfolder, bcupath, 'dataset.csv')

        self.temppath = os.path.join('/', *subfolder, bcupath, 'temp.spc')

        try:
            self.loaddb()
        except:
            self.dataset = pd.DataFrame(columns = self.columns)

    def createdb(self, df, targets):
        sampleid = 0
        self.dataset = pd.DataFrame(columns=self.columns)
        df.sort_values(by='time', ascending=True, inplace=True)
        for index, singleline in df.iterrows():
            line = singleline.to_frame().T

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
            misc = pd.DataFrame(details, index=[index])

            line = pd.concat([line, misc], axis=1)
            #line.to_csv(f'{index}-line.csv')

            self.dataset = self.dataset.append(line, ignore_index=True)

        self.savedb()

    def adddb(self, df):
        pass

    def get_db(self, shape=False):
        """OPtions to come to refine the file"""
        if shape:
            return self.dataset.shape[0]
        return self.dataset


    def savedb(self):
        self.dataset.to_csv(self.bcupath)

    def loaddb(self):
        self.dataset = pd.read_csv(self.bcupath, index_col=0)

    def read_targets(self, filestream):
        """Reads and returns the excel target set"""
        subfolder = basedir.split('/')[:-1]
        temppath = os.path.join('/', *subfolder, 'backup', 'targets.xlsx')
        filestream.save(temppath)
        targets = pd.read_excel(temppath)
        return targets

if __name__ == '__main__':
    databasemng = Databasemng()
