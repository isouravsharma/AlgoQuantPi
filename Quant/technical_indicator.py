import pandas as pd
import numpy as np
import datetime as dt

# RSI 
def RSI(data, n = 14):
    delta = data['Adj Close'] - data['Adj Close'].shift(1)
    gain = (delta.where(delta>=0, 0)).fillna(0)
    loss = (-delta.where(delta <0, 0)).fillna(0)
    avg_gain = gain.ewm(alpha = 1/n, min_periods = n).mean()
    avg_loss = loss.ewm(alpha = 1/n, min_periods = n).mean()
    rs = avg_gain/avg_loss
    rsi = 100-(100/(1+rs))
    data['RSI'] = rsi
    return data
    
#MACD
def MACD(data, a=12, b=26, c=9):
    # data = data.copy()
    data['ma_fast'] = data['Adj Close'].ewm(span = a, min_periods=a).mean()
    data['ma_slow'] = data['Adj Close'].ewm(span = b, min_periods=b).mean()
    data['MACD'] = data['ma_fast'] - data['ma_slow']
    data['SIGNAL'] = data['MACD'].ewm(span=c, min_periods=c).mean()
    # return data.loc[:, ['MACD','SIGNAL']]
    return data

# ATR
def ATR(data, n = 14):
    data['H-L'] = data['High'] - data['Low']
    data['H-PC'] = data['High'] - data['Adj Close'].shift(1)
    data['L-PC'] = data['Low'] - data['Adj Close'].shift(1)
    data["TR"] = data[['H-L','H-PC','L-PC']].max(axis=1, skipna = False)
    data['ATR'] = data['TR'].ewm(span = n, min_periods = n).mean()
    return data

# Bollinger Band
def BB(data, n = 14):
    data['MB'] = data['Adj Close'].rolling(n).mean()
    data['UB'] = data['MB'] + 2* data['Adj Close'].rolling(n).std(ddof = 0)
    data['LB'] = data['MB'] - 2* data['Adj Close'].rolling(n).std(ddof = 0)
    data['WIDTH'] = data['UB'] - data['LB']
    return data

# Linear Regression Band
def calculate_LR(data, ax= None):
    y = np.array(data['Adj Close'])
    X = pd.to_datetime(data[' Adj Close'].index).map(dt.datetime.toordinal)
    X = np.array(X)
    intercept, slope = np.polynomial.polynomial.polyfit(X, y, deg =1)
    regression_line = (slope * X + intercept)
    
    # Calculate standard deviation
    data['STD'] = np.std(y - regression_line)
    data['+1STD'] = regression_line + 1 * data['STD']
    data['-1STD'] = regression_line - 1 * data['STD']
    data['+2STD'] = regression_line + 2 * data['STD']
    data['-2STD'] = regression_line - 2 * data['STD']
    X = pd.to_datetime(data['Adj Close'].index)
    return data