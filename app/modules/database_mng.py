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

class Databasemng():
    """pandas version, sqlite to come"""
    def __init__(self, bcupath = 'backup'):
        self.columns = []
        self.db = pd.DataFrame(columns = self.columns)
        self.bcupath = bcupath

    def createdb(self, df):
        pass

    def adddb(self, df):
        pass

    def get_db(self):
        pass

    def savedb(self):
        pass

    def loaddb(self):
        pass

    def read_targets(self, filestream):
        """Reads and returns the excel target set"""
        targets = pd.read_excel(StringIO(str(filestream.stream.read())))
        print('Yayyy')
        return targets
