import pandas as pd
import numpy as np
import datetime as dt

# RSI 
def calculate_rsi(data, window=14):
    # Calculate the price differences
    delta = data['Close'].diff()

    # Separate the gains and losses
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    # Calculate the rolling averages of gains and losses
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    # Calculate RS (Relative Strength)
    rs = avg_gain / avg_loss

    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    # data['RSI'] = rsi
    return rsi


def calculate_LR(data, ax= None):
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