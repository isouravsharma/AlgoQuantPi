#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:44:02 2025

@author: sousharma
"""

# Calculate Return

import numpy as np
import pandas as pd
def cummulative_returns(data):
    # data = DF.copy()
    #data = pd.DataFrame(data)
    data['d_rtn'] = data['Close'].pct_change()
    data['daily_returns'] = data['Close'].pct_change()
    # data['w_rtn'] = data['Close'].resample('W').ffill().pct_change()
    # data['m_rtn'] = data['Close'].resample('M').ffill().pct_change()
    data['cum_rtn'] =  (1+ data['d_rtn']).cumprod()
    return data

# CAGR

def CAGR(data):
    # data = data.copy()
    n = len(data)/252
    data['CAGR'] =((data['cum_rtn'].iloc[-1]))**(1/n)-1
    return data
    
# Volatility

def volatility(data):
    data['VOL']  = (data['d_rtn'].std()* np.sqrt(252))
    return data

# SHARPE

def SHARPE(data, risk_free):
    # CAGR = CAGR(data)
    data['SHARPE'] = (data['CAGR'] - risk_free)/data['VOL']
    return data

# SORTINO

def SORTINO(data, risk_free):
    neg_return = np.where(data['d_rtn']> 0, 0, data['d_rtn'])
    neg_vol = np.sqrt((pd.Series(neg_return[neg_return!=0])**2).mean() *252)
    data['SORTINO'] = (data['CAGR'] - risk_free)/neg_vol
    return data

# MAXDRAWDOWN
def MAXDROWDOWN(data):
    # data['return'] = data['Close'].pct_change()
    data['cum_return'] = (1+ data['d_rtn']).cumprod()
    data['cum_roll_max'] = data['cum_return'].cummax()
    data['drawdown'] = data['cum_roll_max'] - data['cum_return']
    data['Max_DD'] = ((data['drawdown']/data['cum_roll_max'])).max()*100
    return data

# CALMAR 
def CALMAR(data):
    data['CALMAR'] = data['CAGR']/data['Max_DD']
    return data