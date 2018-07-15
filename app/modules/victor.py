#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:11:04 2018

@author: Laurent Rudloff
"""

__author__ = 'Larry'

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import ElasticNet

class Victor():
    def __init(self, bcupath = 'backup'):
        """Initialize data"""
        self.bcupath = bcupath
        self.scaler = StandardScaler()
        self.pca = PCA()
        self.estimator = ElasticNet(random_state=0)

    def load_model(self):
        """Load the trained models"""
        pass

    def save_model(self):
        """Save the trained model"""
        pass

    def fit(self, X, y):
        """fit the model"""
        pass

    def predict(self, X):
        """Predict from X"""
        pass

if __name__ == '__main__':
    pass
