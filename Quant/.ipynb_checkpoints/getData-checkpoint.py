import yfinance as yf
import datetime


def get_data(ticker, start_date, end_date = datetime.datetime.today().strftime("%Y-%m-%d"), interval = '1d'):
    # ohlc = {}
    download_data = yf.download(tickers = ticker, start = start_date, end = end_date, interval=interval)
    # ohlc[ticker] = download_data
    return download_data

def get_ohlcv(ticker, period, interval, multi_level_index=False):
    data = yf.download(tickers= ticker, period = period, interval = interval, multi_level_index=False)
    data.dropna(how='any', inplace = True)
    return data

# def get_dic_data(ticker, start_date, end_date = datetime.datetime.today().strftime("%Y-%m-%d")):
#     # ohlc = {}
#     download_data = yf.download(tickers = ticker, start = start_date, end = end_date)
#     # ohlc[ticker] = download_data
#     return download_data