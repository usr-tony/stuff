#!./env/bin/python3

from time import time
import pandas as pd
from timeit import timeit
import re
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates
import numpy as np


def main():
    paths = ['./data/BTCUSDT-trades-2022-06-09.csv', './data/TRXUSDT-trades-2022-06-09.csv']
    dfs = []
    for path in paths:
        df = preprocess(path)
        dfs += [add_symbol_name(df, path)]

    merged = merge_dfs(*dfs)
    corr = rolling_corr(merged)
    plot(corr)


def preprocess(path):
    with open(path) as file:
        df = pd.read_csv(file, names=['id', 'price', 'quantity', 'volume', 'time'], usecols=range(5))

    # drop consecutive rows that don't change in price and sum their quantities
    keep_rows = df['price'] != df['price'].shift()
    adjacent_rows = keep_rows.cumsum()
    grouped = df.groupby(adjacent_rows, as_index=False, sort=False)
    quantity = grouped['quantity'].sum()
    df = df[keep_rows].copy()
    df['quantity'] = quantity.to_numpy()
    df['time'] = pd.to_datetime(df['time'] * 10 ** 6)
    return df


def rolling_mod(df):
    temp = df.rolling(window='60s', on='time')
    return df['price'] / temp['price'].mean()


def add_symbol_name(df, path):
    match = re.search('(?<=/)\w+(?=usdt)', path, flags=re.IGNORECASE)
    df['symbol'] = match[0].lower()
    return df


def merge_dfs(df, df2):
    df = pd.concat([df, df2], ignore_index=True)
    df = df.sort_values(by=['time'], ignore_index=True) # may be less efficient than a moving index
    df = df[df['symbol'] != df['symbol'].shift()]
    if df['symbol'][0] == df.iloc[-1]['symbol']:
        df = df.iloc[: -1]

    time_between_trades(df)
    groups = [[symbol, group.reset_index(drop=True)] for symbol, group in df.groupby('symbol')]
    return pd.DataFrame({
        'time': groups[0][1]['time'],
        groups[0][0]: groups[0][1]['price'],
        groups[1][0]: groups[1][1]['price']
    })


def rolling_corr(df):
    rolling = df.rolling(window='120s', on='time')
    corrs = {'time': [], 'corr': []}
    for row in rolling:
        corr = row.iloc[:, 0].corr(row.iloc[:, 1])
        corrs['time'].append(row.index[-1])
        corrs['corr'].append(corr)

    return pd.DataFrame(corrs)


def time_between_trades(df):
    time_diff = df['time'] - df['time'].shift()
    print('time diff:', time_diff.mean())


def plot(df):
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.plot(df.iloc[:, 0], df.iloc[:, 1], linewidth=0.5)
    date_formatter = matplotlib.dates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(date_formatter)
    plt.show()
    

if __name__ == '__main__':
    main()
