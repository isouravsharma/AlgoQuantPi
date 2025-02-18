import yfinance as yf
import datetime


def get_data(ticker, start_date, end_date = datetime.datetime.today().strftime("%Y-%m-%d")):
    # ohlc = {}
    download_data = yf.download(tickers = ticker, start = start_date, end = end_date)
    # ohlc[ticker] = download_data
    return download_data

def get_ohlc(ticker, period, interval):
    data = yf.download(tickers= ticker, period = period, interval = interval)
    data.dropna(how='any', inplace = True)
    return data