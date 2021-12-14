import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.dates as mpl_dates
import mplfinance as mpf
import logging



def clean_df(dataframe):
    df = dataframe
    df['Date'] = pd.to_datetime(df.index)
    # df['Date'] = df['Date'].apply(mpl_dates.date2num)
    
    return df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

def isSupport(df, i):
    support = df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]

    return support


def isResistance(df, i):
    resistance = df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]

    return resistance

def identify_levels(df):
    """
    Returns list of tuples containing:
        - Date
        - Price level
    """
    s = np.mean(df['High'] - df['Low'])
    
    def isFarFromLevel(l, lvls):
        return np.sum([abs(l-x) < s for x in lvls]) == 0


    levels = []
    for i in range(2, df.shape[0]-2):
        if isSupport(df, i):
            l = df['Low'][i]

            if isFarFromLevel(l, levels):
                levels.append((i, df['Low'][i]))

        elif isResistance(df, i):
            l = df['High'][i]

            if isFarFromLevel(l, levels):
                levels.append((i, df['High'][i]))

    return levels

def plot_levels(df, levels):
    xmax = max(df['Date'])

    plot_lines = generate_plot_lines(df, levels)

    mpf.plot(
        df,
        type='candle',
        title='BTC-USD',
        ylabel='Price ($)',
        alines= plot_lines
    )

def generate_plot_lines(df, levels):
    xmax = max(df['Date'])
    plot_lines = []
    
    for level in levels:
        plot_lines.append([(df['Date'][level[0]], level[1]), (xmax, level[1])])

    return plot_lines

def analyze(df):
    df = clean_df(df)
    levels = identify_levels(df)
    plot_levels(df, levels)



def support(df1, l, n1, n2):
    """
    Returns boolean value if candlestick 'l' in dataframe 'df1' is
    a support level. 'n1' and 'n2' are look-back and look-forward 
    values, respectively.
    """

    for i in range(l-n1+1, l+1):
        if(df1.Low[i] > df1.Low[i-1]):
            return 0
        
    for i in range(l+1, l+n2+1):
        if(df1.Low[i] < df1.Low[i-1]):
            return 0

    return 1

def resistance(df1, l, n1, n2):
    """
    Returns boolean value if candlestick 'l' in dataframe 'df1' is
    a resistance level. 'n1' and 'n2' are look-back and look-forward 
    values, respectively.
    """

    for i in range(l-n1+1, l+1):
        if(df1.High[i] < df1.High[i-1]):
            return 0

    for i in range(l+1, l+n2+1):
        if(df1.High[i] > df1.High[i-1]):
            return 0

    return 1

