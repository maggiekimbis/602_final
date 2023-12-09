# -*- coding: utf-8 -*-
"""test2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yeytRv0wk-MGty7b5zyhLxcDQZgfFOdt
"""

import streamlit as st
import requests
import pandas as pd
import io
import seaborn as sns

keys = ['YR7C1B1NPZ97A348', 'JCQFVNBK3U8QMZ0T', 'P1Y9WYCX6JNW4N1M', 'HP94RXLQOYEWVCMZ']
MY_KEY = "HP94RXLQOYEWVCMZ"

st.title('Nintendo And Rockstar Stock Forecast')
stocks = ('NTDOY', 'TTWO')
selected_stock = st.selectbox('Select stock for prediction', stocks)


def fetch_stock_data(symbol, api_key, year_needed):
    DAILY_ENDPOINT = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}&datatype=csv"
    r = requests.get(DAILY_ENDPOINT).content
    df = pd.read_csv(io.StringIO(r.decode('utf-8')))
    df = pd.DataFrame(df)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df[df["timestamp"].dt.year >= year_needed]

    if symbol == "NTDOY":
        share_split_date = pd.to_datetime('10/04/2022')
        before_split = df[df['timestamp'] < share_split_date]
        after_split = df[df['timestamp'] >= share_split_date]
        before_split[['open', 'high', 'low', 'close']] = before_split[['open', 'high', 'low', 'close']] / 5
        adjusted_df = pd.concat([after_split, before_split])
        return adjusted_df
    else:
        return df


def call_data(dataset):
    if dataset == "NTDOY":
        ntdoy_df = fetch_stock_data("NTDOY", MY_KEY, 2007)
        return ntdoy_df
    else:
        ttwo_df = fetch_stock_data("TTWO", MY_KEY, 2007)
        return ttwo_df


choose_dataset = call_data(selected_stock)


def plot_graph(dataset):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='timestamp', y='value', hue='variable',
                 data=pd.melt(dataset, id_vars='timestamp',
                              value_vars=['open', 'high', 'low', 'close']),
                 palette='muted', linewidth=2.5)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{selected_stock} Stock Prices')
    plt.legend(title='Type', loc='upper left')
    return plt


data_graph = plot_graph(choose_dataset)
st.write("Recent five days", choose_dataset.head())

st.pyplot(data_graph)