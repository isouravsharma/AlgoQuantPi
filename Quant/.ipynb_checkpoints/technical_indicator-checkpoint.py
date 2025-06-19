import pandas as pd
import numpy as np
import datetime as dt
from renko import Renko
from scipy.signal import argrelextrema
from scipy.stats import trim_mean

# RSI 
def RSI(df, n = 14):
    data = df.copy()
    delta = data['Close'] - data['Close'].shift(1)
    gain = (delta.where(delta>=0, 0)).fillna(0)
    loss = (-delta.where(delta <0, 0)).fillna(0)
    avg_gain = gain.ewm(alpha = 1/n, min_periods = n).mean()
    avg_loss = loss.ewm(alpha = 1/n, min_periods = n).mean()
    rs = avg_gain/avg_loss
    rsi = 100-(100/(1+rs))
    df['RSI'] = rsi
    return df['RSI']
    
#MACD
def MACD(data, a=12, b=26, c=9):
    # data = data.copy()
    data['ma_fast'] = data['Close'].ewm(span = a, min_periods=a).mean()
    data['ma_slow'] = data['Close'].ewm(span = b, min_periods=b).mean()
    data['MACD'] = data['ma_fast'] - data['ma_slow']
    data['SIGNAL'] = data['MACD'].ewm(span=c, min_periods=c).mean()
    # return data.loc[:, ['MACD','SIGNAL']]
    return data

# ATR
def ATR(data, n = 14):
    df = data.copy()
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = df['High'] - df['Close'].shift(1)
    df['L-PC'] = df['Low'] - df['Close'].shift(1)
    df["TR"] = df[['H-L','H-PC','L-PC']].max(axis=1, skipna = False)
    data['ATR'] = df['TR'].ewm(span = n, min_periods = n).mean()
    return data['ATR']

#RENKO


def RENKO(data):
    "function to convert ohlc data into renko bricks"
    df = data.copy()
    df.reset_index(inplace=True)
    df = df.iloc[:,[0,1,2,3,4,5]]
    df.columns = ["date","open","high","low","close","volume"]
    df2 = Renko(df)
    df2.brick_size = max(0.5,round(ATR(DF,120)["ATR"][-1],0))
    renko_df = df2.get_ohlc_data()
    renko_df["bar_num"] = np.where(renko_df["uptrend"]==True,1,np.where(renko_df["uptrend"]==False,-1,0))
    for i in range(1,len(renko_df["bar_num"])):
        if renko_df["bar_num"][i]>0 and renko_df["bar_num"][i-1]>0:
            renko_df["bar_num"][i]+=renko_df["bar_num"][i-1]
        elif renko_df["bar_num"][i]<0 and renko_df["bar_num"][i-1]<0:
            renko_df["bar_num"][i]+=renko_df["bar_num"][i-1]
    renko_df.drop_duplicates(subset="date",keep="last",inplace=True)
    return renko_df


#ADX
def ADX(data, n = 14):
    data['UPMOVE'] = data['High'] - data['High'].shift(1)   
    data['DOWNMOVE'] = data['Low'].shift(1) - data['Low']
    data['+DM'] = np.where((data['UPMOVE']> data['DOWNMOVE']) & (data['UPMOVE']> 0), data['UPMOVE'],0)
    data['-DM'] = np.where((data['DOWNMOVE']> data['UPMOVE']) & (data['DOWNMOVE']> 0), data['DOWNMOVE'],0)
    data['+DI'] = 100 * (data['+DM']/data['ATR']).ewm(alpha=1/n, min_periods = n).mean()
    data['-DI'] = 100 * (data['-DM']/data['ATR']).ewm(alpha=1/n, min_periods = n).mean()
    data['ADX'] = 100 * abs((data['+DI'] - data['-DI'])/(data['+DI'] + data['-DI'])).ewm(span = n, min_periods = n).mean()
    return data
    
# Bollinger Band
def BB(data, n = 14):
    # df = data.copy()
    # data['MB'] = data['Close'].rolling(n).mean()
    data['MB'] = data['Close'].rolling(n).apply(lambda x: trim_mean(x, proportiontocut = 0.15), raw=True)
    data['STD'] = data['Close'].rolling(n).std(ddof = 0)
    data['UB'] = data['MB'] + 2* data['STD']
    data['LB'] = data['MB'] - 2* data['STD']
    data['WIDTH'] = data['UB'] - data['LB']
    return data[['MB','UB','LB','STD','WIDTH']]

# # Bollinger Band - Normal Mean
# def BB(data, n = 14):
#     # df = data.copy()
#     data['MB'] = data['Close'].rolling(n).mean()
#     data['STD'] = data['Close'].rolling(n).std(ddof = 0)
#     data['UB'] = data['MB'] + 2* data['STD']
#     data['LB'] = data['MB'] - 2* data['STD']
#     data['WIDTH'] = data['UB'] - data['LB']
#     return data[['MB','UB','LB','STD','WIDTH']]

# Linear Regression Band
def LR(data, ax= None):
    y = np.array(data['Close'])
    X = pd.to_datetime(data['Close'].index).map(dt.datetime.toordinal)
    X = np.array(X)
    intercept, slope = np.polynomial.polynomial.polyfit(X, y, deg =1)
    regression_line = (slope * X + intercept)
    
    # Calculate standard deviation
    data['STD'] = np.std(y - regression_line)
    data['+1STD'] = regression_line + 1 * data['STD']
    data['-1STD'] = regression_line - 1 * data['STD']
    data['+2STD'] = regression_line + 2 * data['STD']
    data['-2STD'] = regression_line - 2 * data['STD']
    X = pd.to_datetime(data['Close'].index)
    return data
#Anomaly

def anomaly(data):
    df = data.copy()
    window = 16
    threshold = 2.7
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Rolling_Mean'] = df['Log_Return'].rolling(window).mean()
    df['Rolling_STD'] = df['Log_Return'].rolling(window).std()
    df['Z_Score'] = (df['Log_Return'] - df['Rolling_Mean']) / df['Rolling_STD']
    df['Anomaly'] = (df['Z_Score'] > threshold) | (df['Z_Score'] < -threshold)
    data['Anomaly'] = df['Anomaly']
    data['Log_Return'] = df['Log_Return']
    data['Z_Score'] = df['Z_Score']
    return data[['Anomaly','Log_Return','Z_Score']]
    
def historical_volatility(data, window=14):
    # Rolling standard deviation
    volatility = data['Log_Return'].rolling(window).std() * np.sqrt(252)  # annualized
    data['volatility'] = volatility
    return data['volatility']

def get_support_resistance_levels(data, order=14):
    # Local minima as support
    support_idx = argrelextrema(data['Low'].values, np.less_equal, order=order)[0]
    support_levels = data['Low'].iloc[support_idx]

    # Local maxima as resistance
    resistance_idx = argrelextrema(data['High'].values, np.greater_equal, order=order)[0]
    resistance_levels = data['High'].iloc[resistance_idx]

    return support_levels, resistance_levels

def VWAP(data):
    # Step 1: Calculate Typical Price (Series)
    data['TP'] = (data['High'] + data['Low'] + data['Close']) / 3
    
    # Step 2: Cumulative volume and cumulative price*volume
    data['cum_vol'] = data['Volume'].cumsum()
    data['cum_pv'] = (data['TP'] * data['Volume']).cumsum()
    # data['cum_pv'] = np.multiply(data['TP'].values, data['Volume'].values).cumsum()
    # Step 3: VWAP
    data['VWAP'] = data['cum_pv'] / data['cum_vol']
    return data['VWAP']