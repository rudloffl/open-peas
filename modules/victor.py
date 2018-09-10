#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:11:04 2018

@author: Laurent Rudloff
"""

__author__ = 'Larry'

import numpy as np
import pandas as pd

import os

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import ElasticNet
from scipy.special import inv_boxcox
from scipy import stats
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
import pickle

from hyperopt import hp, tpe
from hyperopt.fmin import fmin

basedir = os.path.abspath(os.path.dirname(__file__))

class Victor():
    def __init__(self, bcupath = 'backup', cv=3, max_evals=20):
        """Initialize data"""
        subfolder = basedir.split('/')[:-1]
        self.bcupath = os.path.join('/', *subfolder, bcupath)

        #self.load_model()
        try:
            self.load_model()
        except:
            self.scaler = StandardScaler()
            self.pca = PCA()
            self.estimator = ElasticNet(random_state=0)
            self.rmsecv = 1e20
            self.trained = False
            self.cv = cv
            self.columns = ['wl_{}'.format(x) for x in range(950, 1530+1, 2)]
            self.max_evals = max_evals
            self.lmbda = 0


    def load_model(self):
        """Load the trained models"""
        with open(os.path.join(self.bcupath, 'misc-estimator.pkl'), 'rb') as handle:
            saved = pickle.load(handle)

        self.rmsecv = saved['rmsecv']
        self.trained = saved['trained']
        self.cv = saved['cv']
        self.columns = saved['columns']
        self.lmbda = saved['lmbda']
        self.max_evals = saved['max_evals']

        self.scaler = joblib.load(os.path.join(self.bcupath, 'scaler.pkl'))
        self.pca = joblib.load(os.path.join(self.bcupath, 'pca.pkl'))
        self.estimator = joblib.load(os.path.join(self.bcupath, 'estimator.pkl'))
        #print('loaded :', self.scaler.mean_)

    def save_model(self):
        """Save the trained model"""
        tosave = {'rmsecv':self.rmsecv,
                  'trained':self.trained,
                  'cv':self.cv,
                  'columns':self.columns,
                  'lmbda':self.lmbda,
                  'max_evals':self.max_evals,}

        with open(os.path.join(self.bcupath, 'misc-estimator.pkl'), 'wb') as handle:
            pickle.dump(tosave, handle, protocol=pickle.HIGHEST_PROTOCOL)

        #print('saved : ', self.scaler.mean_)
        joblib.dump(self.scaler, os.path.join(self.bcupath, 'scaler.pkl'))
        joblib.dump(self.pca, os.path.join(self.bcupath, 'pca.pkl'))
        joblib.dump(self.estimator, os.path.join(self.bcupath, 'estimator.pkl'))

    def fit(self, dataset):
        """fit the model"""

        X = dataset[self.columns]
        y = dataset['target']

        ybc, self.lmbda = stats.boxcox(y)

        ## HyperOpt features
        def objective(params):
            hyperparams = {
                'alpha': params['alpha'],
                'l1_ratio': params['l1_ratio'],
                'random_state': 0,
                }

            elnet = ElasticNet(**hyperparams)
            scaler = StandardScaler()
            pca = PCA(random_state=0)

            Xscaled = scaler.fit_transform(X)
            Xpca = pca.fit_transform(Xscaled)

            preds = cross_val_predict(elnet, Xpca, ybc, cv=self.cv, n_jobs=-2)
            score = mean_squared_error(inv_boxcox(preds, self.lmbda), y)

            return score

        space = {
            'alpha': hp.loguniform('alpha', -10, 2),
            'l1_ratio': hp.loguniform('l1_ratio',-20, 0),
                }

        best = fmin(fn=objective,
                    space=space,
                    algo=tpe.suggest,
                    max_evals=self.max_evals)

        ## Hyperopt best results and training
        params = {
                'alpha': best['alpha'],
                'l1_ratio': best['l1_ratio'],
                'random_state': 0,
                }

        print(params)

        self.estimator.set_params(**params)
        Xscaled = self.scaler.fit_transform(X)
        Xpca = self.pca.fit_transform(Xscaled)
        self.estimator.fit(Xpca, ybc)

        ## Performance measurement
        self.trained = True
        preds = cross_val_predict(self.estimator, Xpca, ybc, cv=self.cv, n_jobs=-2)
        self.rmsecv = mean_squared_error(inv_boxcox(preds, self.lmbda), y)**.5

        ## save the model
        self.save_model()


    def predict(self, dataset):
        """Predict from X"""
        X = dataset[self.columns]
        Xscaled = self.scaler.transform(X)
        Xpca = self.pca.transform(Xscaled)
        predsbc = self.estimator.predict(Xpca)
        return inv_boxcox(predsbc, self.lmbda)

if __name__ == '__main__':
    victor = Victor()
    dataset = pd.read_csv('../backup/dataset.csv')
    #print(dataset.shape)
    #victor.fit(dataset)
    print('rmse : {}'.format(victor.rmsecv))
    print('trained : {}'.format(victor.trained))
    print('preds: {}'.format(victor.predict(dataset)))
    print('pred: {}'.format(victor.predict(dataset.iloc[3].to_frame().T)))
