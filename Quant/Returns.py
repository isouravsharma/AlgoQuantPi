#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:44:02 2025

@author: sousharma
"""

# Calculate Return

import numpy as np
def cummulative_returns(data):
    #data = pd.DataFrame(data)
    data['d_rtn'] = data['Close'].pct_change()
    # data['w_rtn'] = data['Close'].resample('W').ffill().pct_change()
    # data['m_rtn'] = data['Close'].resample('M').ffill().pct_change()
    data['cum_rtn'] = ((1+ data['d_rtn']).cumprod() -1)*100
    return data

# CAGR

def CAGR(data):
    n = len(data)/252
    data['CAGR'] = np.abs((data['cum_rtn'].iloc[-1]))**(1/n)-1
    return data
    
# Volatility

def volatility(data):
    data['vol']  = data['d_rtn'].std()*np.sqrt(252)
    return data

