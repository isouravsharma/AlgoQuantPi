#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 15:44:02 2025

@author: sousharma
"""

# Calculate Return

def cummulative_returns(data):
    #data = pd.DataFrame(data)
    data['d_rtn'] = data['Close'].pct_change()
    # data['w_rtn'] = data['Close'].resample('W').ffill().pct_change()
    # data['m_rtn'] = data['Close'].resample('M').ffill().pct_change()
    data['cum_rtn'] = ((1+ data['d_rtn']).cumprod() -1)*100
    return data

# (1 + data['Daily Return']).cumprod() - 1

# cummulative Return

# Trade Return

