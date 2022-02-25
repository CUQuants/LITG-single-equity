import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def find_n_return_rf(df):


    N = len(df) + 1
    return_series = df[df.columns[0]].pct_change()
    rf = df[df.columns[len(df.columns) - 1]][len(df) - 1]
   
    return N, return_series, rf

def sharpe_ratio(return_series, N, rf):
   
    mean = return_series.mean() * N -rf
    sigma = return_series.std() * np.sqrt(N)
   
    return mean / sigma

def sortino_ratio(series, N,rf):
   
    mean = series.mean() * N -rf
    std_neg = series[series<0].std()*np.sqrt(N)
   
    return mean/std_neg

def max_drawdown(return_series):
   
    comp_ret = (return_series+1).cumprod()
    peak = comp_ret.expanding(min_periods=1).max()
    dd = (comp_ret/peak)-1
   
    return dd.min()

st.set_page_config(layout = "wide")

def sharpe_ratio(return_series, N, rf):
   
    mean = (return_series.mean() * N) -rf
    sigma = return_series.std() * np.sqrt(N)
   
    return mean / sigma

def sortino_ratio(series, N,rf):
   
    mean = series.mean() * N -rf
    std_neg = series[series<0].std()*np.sqrt(N)
   
    return mean/std_neg

def max_drawdown(return_series):
   
    comp_ret = (return_series+1).cumprod()
    peak = comp_ret.expanding(min_periods=1).max()
    dd = (comp_ret/peak)-1
   
    return dd.min()

def find_n_return_rf(df):


    N = len(df) + 1
    return_series = df[df.columns[0]].pct_change()
    rf = df[df.columns[len(df.columns) - 1]][len(df) - 1]
   
    return N, return_series, rf

def find_color(value, threshold):
   
    if value > threshold:
        color = "green"
       
    if value < threshold:
        color = "red"
       
    return color


def rolling_sharpe(N, return_series):
   
    N = int(N)
    rolling = return_series.rolling(window = int(N))
    rolling_sharpe = np.sqrt(N) * ((rolling.mean())/ rolling.std())
   
    return rolling_sharpe

function_list = ["Investment Statistics"]

st.header("Leeds Investment Trading Group: Single Equity Analysis Tool")
with st.expander('Purpose'):
    st.write("This tool is built for the Leeds Investment Trading Group to analyze single equities")

today = dt.date.today()

before = today - dt.timedelta(days = 365 * 2)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)

if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')                    

sidebar_function = st.sidebar.selectbox("select a function", function_list)

ticker = st.text_input("Please enter ticker here:")
st.text("ex for Microsoft: MSFT")
tickers = [ticker, "^TNX"]
status_radio = st.radio('Please click run when you are ready.', ('stop', 'run'))

if status_radio == "run":
   
    df = yf.download(tickers, start_date, end_date)['Close']
    df["^TNX"] = df["^TNX"] / 100
    N, return_series, rf = find_n_return_rf(df)
   
    col1, col2, col3, col4 = st.columns(4)
   
    with col1:
       
        sharpe_ratio = round(sharpe_ratio(return_series, N, rf),2)
        color = find_color(sharpe_ratio, 1)
        st.title("Sharpe Ratio")
        st.markdown("<h2 style='text-align: left; color: {};'>{}</h2>".format(color, sharpe_ratio), unsafe_allow_html=True)
       
    with col2:
       
        sortino_ratio = round(sortino_ratio(return_series, N, rf),2)
        color = find_color(sortino_ratio, 2)
        st.title("Sortino Ratio:")
        st.markdown("<h2 style='text-align: left; color: {};'>{}</h2>".format(color, sharpe_ratio), unsafe_allow_html=True)
       
    with col3:
       
        max_drawdown = round(max_drawdown(return_series),2)
        color = find_color(max_drawdown, 1)
        st.title("Max Drawdown:")
        st.markdown("<h2 style='text-align: left; color: {};'>{}</h2>".format(color, max_drawdown), unsafe_allow_html=True)
       
    with col4:
       
        calmer = round(return_series.mean()*252/abs(max_drawdown),2)
        color = find_color(calmer, 0.5)
        st.title("Calmer Ratio:")
        st.markdown("<h2 style='text-align: left; color: {};'>{}</h2>".format(color, calmer), unsafe_allow_html=True)
       
    df["6_mon_sharpe"] = rolling_sharpe(252 / 2, return_series)
    df["1_year_sharpe"] = rolling_sharpe(252, return_series)
    st.title("This is Wrong")
    fig = px.line(df, x=df.index, y= df.columns[2:], title='Rolling Sharpe', width = 1500, height = 500)
    st.plotly_chart(fig)
   
    st.title("Things to keep in mind")
    st.header("The risk free rate (10Y)")
    df = df.rename(columns = {"^TNX":"10Y Treasury Yield"})
    df["10Y Treasury Yield"] = df["10Y Treasury Yield"] * 100
    fig = px.line(df, x=df.index, y= df.columns[1], width = 1500, height = 500)
    st.plotly_chart(fig)
