from getData import  get_ohlcv
from technical_indicator import LR, RSI
from Returns import cummulative_returns, CAGR
import copy

tickers = ['^NSEI', 'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'BHARTIARTL.NS', 'ICICIBANK.NS', 'INFY.NS', 'SBIN.NS', 'HINDUNILVR.NS', 
           'BAJFINANCE.NS',
           'ITC.NS']

# Store data in dictionary
ohlcv_dict = {}
for stock in tickers:
    ohlcv_dict[stock] = get_ohlcv(ticker=stock, period = '10y', interval='1d')


data = copy.deepcopy(ohlcv_dict)




# def cummulative_returns(data):
#     print(data)
#     #data = pd.DataFrame(data)
#     daily_return = data['Close'].pct_change()
#     cum_return =  ((1+ daily_return).cumprod() -1)*100
#     data[stock]['d_rtn'] = daily_return
#     data[stock]['cum_rtn'] = cum_return
#     return data

# Analysis of Returns 

for stock in data.keys():
    # print(f"CAGR of stock {stock} is {CAGR(data[stock])}")
    # print(f"CUM RETURN of stock {stock} is {cummulative_returnss()}")
    cummulative_returns(data[stock])
    # CAGR(data[stock])


# DF = data['ICICIBANK.NS']


    


# CAGR

def CAGR(data):
    # data.copy()
    n = len(data[stock])/252
    data[stock]['CAGR'] = np.abs((data[stock]['cum_rtn'].iloc[-1]))**(1/n)-1
    return True

print(data.keys())

cummulative_returns(data['^NSEI'])

data['^NSEI']['Close'].pct_change()