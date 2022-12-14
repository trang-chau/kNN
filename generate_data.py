#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 12:26:19 2018

@author: trang
"""


""" generate_data.py: Use the dynamical models to generate true state, noisy observations and catalog of numerical simulations. """


import numpy as np


def generate_data(x0,f,h,Q,R,dt_int,dt_model,var_obs, T_burnin, T_train, T_test, num_seed):
    """ Generate the true state, noisy observations and catalog of numerical simulations. """

    # initialization
    class X_train:
        values=[]
        time=[];
    class Y_train:
        values=[]
        time=[];
    class X_test:
        values = [];
        time = [];
    class Y_test:
        values = [];
        time = [];
    
    
#    # test on parameters
#    if dt_model>dt_obs:
#        print('Error: dt_obs must be bigger than dt_model');
#    if (np.mod(dt_obs,dt_model)!=0):
#        print('Error: dt_obs must be a multiple of dt_model');
    if ~np.isnan(num_seed): 
        np.random.seed(num_seed)
    # 5 time steps (to be in the attractor space)
    dx = x0.size
    x = np.zeros((dx,T_burnin))
    x[:,0] = x0
    for t in range(T_burnin-1):
        xx = x[:,t]
        for  i in range(dt_model):
            xx = f(xx)
        x[:,t+1] = xx + np.random.multivariate_normal(np.zeros(dx),Q)
    x0 = x[:,-1];

    # generate true state (X_train+X_test)
    T = T_train+T_test
    X = np.zeros((dx,T))
    X[:,0] = x0
    for t in range(T-1):
        XX = X[:,t]
        for  i in range(dt_model):
            XX = f(XX)
        X[:,t+1] = XX + np.random.multivariate_normal(np.zeros(dx),Q)
    # generate  partial/noisy observations (Y_train+Y_test)    
    Y = X*np.nan
    yo = np.zeros((dx,T))
    for t in range(T-1):
        yo[:,t]= h(X[:,t+1]) + np.random.multivariate_normal(np.zeros(dx),R)
    Y[var_obs,:] = yo[var_obs,:];
    
    # Create training data (catalogs)
    ## True catalog
    X_train.time = np.arange(0,T_train*dt_model*dt_int,dt_model*dt_int);
    X_train.values = X[:, 0:T_train];
    ## Noisy catalog
    Y_train.time = X_train.time[1:];
    Y_train.values = Y[:, 0:T_train-1]

    # Create testinging data 
    ## True catalog
    X_test.time = np.arange(0,T_test*dt_model*dt_int,dt_model*dt_int);
    X_test.values = X[:, T-T_test:]; 
    ## Noisy catalog
    Y_test.time = X_test.time[1:];
    Y_test.values = Y[:, T-T_test:-1]; 
 
    

    # reinitialize random generator number
    np.random.seed()

    return X_train, Y_train, X_test, Y_test,yo;


    
    

def generate_data_diff_nDist(x0,f,h,Q,R,dt_int,dt_model,var_obs, T_burnin, T_train, T_test, num_seed, mod_info, obs_info): 

    """ Generate the true state, noisy observations and catalog of numerical simulations with different distributions of noises. """                                      
    
    
    # initialization
    class X_train:
        values=[]
        time=[];
    class Y_train:
        values=[]
        time=[];
    class X_test:
        values = [];
        time = [];
    class Y_test:
        values = [];
        time = [];
    
    
#    # test on parameters
#    if dt_model>dt_obs:
#        print('Error: dt_obs must be bigger than dt_model');
#    if (np.mod(dt_obs,dt_model)!=0):
#        print('Error: dt_obs must be a multiple of dt_model');
    if ~np.isnan(num_seed): 
        np.random.seed(num_seed)
    # 5 time steps (to be in the attractor space)
    dx = x0.size
#     x = np.zeros((dx,T_burnin))
#     x[:,0] = x0
#     for t in range(T_burnin-1):
#         xx = x[:,t]
#         for  i in range(dt_model):
#             xx = f(xx)
#         if mod_info.dist == 'Gaussian':
#             noise_X = np.random.multivariate_normal(np.zeros(dx),Q)
#         if mod_info.dist == 'Student-t':
#             noise_X = np.sqrt(Q/mod_info.pars) * np.random.standard_t(mod_info.pars,size=1) #t.rvs(df, size=1000)
#         x[:,t+1] = xx + noise_X
#     x0 = x[:,-1];

    # generate true state (X_train+X_test)
    T = T_train+T_test + T_burnin
    X = np.zeros((dx,T))
    X[:,0] = x0
    for t in range(T-1):
        XX = X[:,t]
        for  i in range(dt_model):
            XX = f(XX)
        if mod_info.dist == 'Gaussian':
            noise_X = np.random.multivariate_normal(np.zeros(dx),Q)
        if mod_info.dist == 'Student-t':
            noise_X = np.sqrt(Q*(mod_info.pars-2)/mod_info.pars) * np.random.standard_t(mod_info.pars,size=1) #t.rvs(df, size=1000)            
        X[:,t+1] = XX + noise_X
    # generate  partial/noisy observations (Y_train+Y_test)    
    Y = X*np.nan
    yo = np.zeros((dx,T))
    for t in range(T-1):
        if obs_info.dist == 'Gaussian':
            noise_Y = np.random.multivariate_normal(np.zeros(dx),R)
        if obs_info.dist == 'Student-t':
            noise_Y = np.sqrt(R*(obs_info.pars-2)/obs_info.pars) * np.random.standard_t(obs_info.pars,size=1) #t.rvs(df, size=1000)        
        yo[:,t]= h(X[:,t+1]) + noise_Y
    Y[var_obs,:] = yo[var_obs,:];
    
    # Create training data (catalogs)
    ## True catalog
    X_train.time = np.arange(0,T_train*dt_model*dt_int,dt_model*dt_int);
    X_train.values = X[:, T_burnin:(T_train+T_burnin)];
    ## Noisy catalog
    Y_train.time = X_train.time[1:];
    Y_train.values = Y[:, T_burnin:(T_train+T_burnin-1)]

    # Create testinging data 
    ## True catalog
    X_test.time = np.arange(0,T_test*dt_model*dt_int,dt_model*dt_int);
    X_test.values = X[:, T-T_test:]; 
    ## Noisy catalog
    Y_test.time = X_test.time[1:];
    Y_test.values = Y[:, T-T_test:-1]; 
 
    

    # reinitialize random generator number
    np.random.seed()

    return X_train, Y_train, X_test, Y_test,yo;
