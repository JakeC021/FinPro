import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf


# Computer the log returns
def get_hist_data(tickers, start_date, end_date=None, interval='1wk', original_data=False):
    ticker_number = len(tickers.values())

    # 1. Store tickers' returns in Obj his_data
    hist_data = {}
    for key, value in tickers.items():
        hist_data[key] = yf.Ticker(value).history(
            interval=interval, start=start_date, end=end_date)

    # 2. Make sure every dataset has the same length
        # 2.1 Find the number of rows of shortest ticker data
    datalength = []
    for ele in hist_data.values():
        datalength.append(len(ele['Close']))

    min_len = min(datalength)

    # 3. Retrive close data and put into dataframe
    ticker_close_price = {}
    for key, value in hist_data.items():
        # Retrive Index of Date refences to the first ticker's index
        if key == list(hist_data.keys())[0]:
            global idx
            idx = value['Close'][-min_len:].index.date
        ticker_close_price[key] = list(value['Close'][-min_len:])

    df = pd.DataFrame(ticker_close_price,
                      columns=ticker_close_price.keys(),
                      index=idx)

    if original_data == False:
        return df
    else:
        return df, hist_data


def get_ticker_info(tickers):
    data_info = []

    for ticker in tickers.values():
        data_info.append(yf.Ticker(ticker).info)

    df = pd.DataFrame(data_info, index=list(tickers.keys()))

    return df


def log_return(df):
    for col in df.columns:
        if 'LogRets' not in col:
            df[col+'_LogRets'] = np.log(df[col]/df[col].shift(1))

    ret_cols = [col for col in df.columns if 'LogRets' in col]

    # Drop the row where the return value is nan
    rmIdx = df[df[ret_cols[0]].isna()].index
    df.drop(index=rmIdx, inplace=True)

    return df


def cum_return(df):
    for col in [col for col in df.columns if 'LogRets' in col and 'Cum' not in col]:
        df[col+'_Cum'] = np.cumsum(df[col])

    return df
