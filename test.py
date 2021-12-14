"""
DataScience article on Support/Resistance detection
https://towardsdatascience.com/detection-of-price-support-and-resistance-levels-in-python-baedc44c34c9

KrakenAPI Tutorial
https://algotrading101.com/learn/kraken-api-guide/

pykrakenapi Documentation
https://github.com/dominiktraxl/pykrakenapi

yfinance - Cryptocurrency guide
https://medium.com/analytics-vidhya/python-how-to-get-bitcoin-data-in-real-time-less-than-1-second-lag-38772da43740

"""

#from strategy import *
import krakenex
from pykrakenapi import KrakenAPI
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from patterns import *


df = yf.download(tickers='BTC-USD', period = '1y', interval = '1h')

def macd(dataframe, sma_small=10, sma_large=30):
    df = dataframe.drop(columns=['Open', 'High', 'Low', 'Adj Close', 'Volume'])
    df['ma_split'] = df['Close'].rolling(window=sma_small).mean() - df['Close'].rolling(window=sma_large).mean()
    df['compare'] = df['ma_split'].shift(periods=1)
    df.dropna(subset=['ma_split', 'compare'])

    signals = []

    for i in df.index:
        if df.loc[i,'ma_split'] > 0 and df.loc[i, 'compare'] < 0:
            signals.append((i, df.loc[i, 'Close'], 1))
        elif df.loc[i,'ma_split'] < 0 and df.loc[i, 'compare'] > 0:
            signals.append((i, df.loc[i, 'Close'], 0))

    return signals

data = macd(df, 10, 30)
print(len(data))